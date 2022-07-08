import tempfile
import pyodbc
import requests
from datetime import datetime
import os
from os.path import join
import csv
import logging
from .email import send_email_to
from concurrent.futures import ThreadPoolExecutor
import concurrent
from .azure_storage import upload_local_file
from .config import *


def request_to_ureditos(**kwargs) -> requests.Response:
    """
    Make a request with input arguments as params.
    """
    params = {
        'wstoken': API_UREDITOS_TOKEN,
        'moodlewsrestformat': 'json',
    }
    params.update(kwargs)
    try:
        response = requests.get(url=URL_API_UREDITOS,
                                params=params, timeout=10)
    except Exception as e:
        logging.info(f'Request has thrown an error:{e}')
        response = requests.Response()
        response.status_code = 400
        return response
    else:
        return response


def query_database(query: str) -> list:
    """
    Make a query to DB_NAME database of SQL Server DB_HOST.
    """
    # Database connection
    os_name = os.name
    if os_name == 'nt':
        conn_string = f'Driver={{SQL Server}};Server={DB_HOST};Database={DB_NAME};UID={DB_USERNAME};PWD={DB_PASSWORD}'
    else:
        conn_string = f'Driver={{ODBC Driver 17 for SQL Server}};Server={DB_HOST};Database={DB_NAME};UID={DB_USERNAME};PWD={DB_PASSWORD}'

    conn = pyodbc.connect(conn_string)
    cursor = conn.cursor()

    # Execution of query in Database. Fetch results in results variable.
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return results


def enrolling_moodle():
    """
    Executes enrolling of users in moodle courses by results of a query to database DB_NAME.
    """
    # Today's date
    today = datetime.now()

    # Today's month
    month = MONTHS.get(today.month)

    # Definition of tempdir path.
    folder = tempfile.gettempdir()

    # Build query to database
    query = f"SELECT * FROM {TABLA_CONSOLIDADO} WHERE Ejecucion = '{month}-{today.year}' ORDER BY Zona"

    # Make query to database
    query_results = query_database(query)

    # Definition of csv and txt file paths.
    csv_log = join(folder, f'logMoodle{today.strftime("%Y-%m-%d-%H")}h.csv')
    txt_log = join(folder, 'logMoodleAcciones.txt')

    with open(csv_log, mode='w', newline='') as csv_file, open(txt_log, mode='a') as txt:
        fields = ['username', 'user_id',
                  'course', 'course_id', 'status']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fields)
        csv_writer.writeheader()
        txt.write(f'[{datetime.now()}] Inicio proceso de matriculacion.\n')

        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = [executor.submit(
                requests_for_enrolling_moodle, row) for row in query_results]

            for future in concurrent.futures.as_completed(futures):
                try:
                    data = future.result()
                    logging.info(f'User {data.get("username")} enrolled.')
                except Exception as e:
                    logging.info(f'Exception ocurred: {e}')
                else:
                    csv_writer.writerow({'username': data.get('username'), 'user_id': data.get('user_id'),
                                        'course': data.get('course'), 'course_id': data.get('course_id'), 'status': f'{data.get("endpoint")} {data.get("status")}'})

        txt.write(f'[{datetime.now()}] Fin proceso de matriculacion.\n')

    # Execute uploading function for creating a csv log on file share resource
    upload_local_file(CONNECT_STRING, csv_log, SHARE_NAME, join(
        'logsMoodle', f'logMoodle{today.strftime("%Y-%m-%d-%H")}h.csv'))
    # Execute uploading function for creating a log on file share resource
    upload_local_file(CONNECT_STRING, txt_log,
                      SHARE_NAME, 'logMoodleAcciones.txt')


def send_sms_notifications():
    """
    Executes sms notifications module. 
    """
    # Today's date
    today = datetime.now()

    # Today's month
    month = MONTHS.get(today.month)

    # Definition of tempdir path.
    folder = tempfile.gettempdir()

    # Build query to database
    query = f"SELECT * FROM {TABLA_CONSOLIDADO} WHERE Ejecucion = '{month}-{today.year}' ORDER BY Zona"

    # Make query to database
    query_results = query_database(query)

    # Definition of csv and txt file paths.
    csv_log = join(folder, f'logAvisosSMS{today.strftime("%Y-%m-%d-%H")}h.csv')
    txt_log = join(folder, 'logMoodleAcciones.txt')

    # Declare a dict with params to insert into request to Masivapp API.
    params = {
        'action': 'sendmessage',
        'username': API_MASIVAPP_USERNAME,
        'password': API_MASIVAPP_PASSWORD,
        'longMessage': 'false',
        'flash': 'false',
        'premium': 'false'
    }

    with open(csv_log, mode='w', newline='') as csv_file, open(txt_log, mode='a') as txt:
        fields = ['username', 'user_id',
                  'course', 'course_id', 'status']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fields)
        csv_writer.writeheader()
        txt.write(f'[{datetime.now()}] Inicio proceso de SMS.\n')

        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = [executor.submit(
                requests_for_sms_notifications, row, params) for row in query_results]
            for future in concurrent.futures.as_completed(futures):
                try:
                    data = future.result()
                    logging.info(f'User {data.get("username")} notified.')
                except Exception as e:
                    logging.info(f'Exception ocurred: {e}')
                else:
                    csv_writer.writerow({'username': data.get('username'), 'user_id': data.get('user_id'),
                                        'course': data.get('course'), 'course_id': data.get('course_id'), 'status': f'{data.get("endpoint")} {data.get("status")}'})

        txt.write(f'[{datetime.now()}] Fin proceso de SMS.\n')

    # Execute uploading function for creating a csv log on file share resource
    upload_local_file(CONNECT_STRING, csv_log, SHARE_NAME, join(
        'logsSms', f'logAvisosSMS{today.strftime("%Y-%m-%d-%H")}h.csv'))
    # Execute uploading function for creating a log on file share resource
    upload_local_file(CONNECT_STRING, txt_log,
                      SHARE_NAME, 'logMoodleAcciones.txt')


def send_email_notifications():
    """
    Executes email notifications module. 
    """
    # Today's date
    today = datetime.now()

    # Today's month
    month = MONTHS.get(today.month)

    # Definition of tempdir path.
    folder = tempfile.gettempdir()

    # Build query to TABLA_CONSOLIDADO and order by Zona
    query = f"SELECT * FROM {TABLA_CONSOLIDADO} ORDER BY Zona"

    # Make query to database
    query_results = query_database(query)
    # logging.info(f'query results:{query_results}')

    # Build query to TABLA_CONSOLIDADO for getting email recipients
    query = f"SELECT DISTINCT CorreoElectronico FROM {TABLA_CONSOLIDADO}"

    # Make query and retrieve recipients results
    recipients = query_database(query)
    # Extact first element of tuple list to build a list of recipients
    recipients = [row[0] for row in recipients]

    # Definition of csv and txt file paths.
    csv_log = join(
        folder, f'UReditos_Consolidado_Inscripciones {today.strftime("%Y-%m-%d")}.csv')
    txt_log = join(folder, 'logMoodleAcciones.txt')

    with open(csv_log, mode='w', newline='') as csv_file:
        fields = ['Id', 'Nombre asesor(a)', 'Zona',
                  'Oficina', 'Nombre curso', 'Estado']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fields)
        csv_writer.writeheader()

    with open(txt_log, mode='a') as txt:
        txt.write(f'[{datetime.now()}] Inicio proceso de correos.\n')

        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = [executor.submit(
                email_csv_report_writer, row, csv_log) for row in query_results]

        # Execute function for sending email to all coordinators.
        send_email_to(recipients, csv_log)
        txt.write(f'[{datetime.now()}] Fin proceso de correos.\n')

    # Execute uploading function for creating a csv log on file share resource
    upload_local_file(CONNECT_STRING, csv_log, SHARE_NAME, join(
        'logsCorreo', f'UReditos_Consolidado_Inscripciones {today.strftime("%Y-%m-%d")}.csv'))
    # Execute uploading function for creating a log on file share resource
    upload_local_file(CONNECT_STRING, txt_log,
                      SHARE_NAME, 'logMoodleAcciones.txt')


def requests_for_enrolling_moodle(row: list) -> dict:
    """
    Make the required requests to retrieve data for enrolling students.
    Receives a row from query database results list.
    Returns a dictionary with data from requests to Ureditos.
    """
    data = {
        'username': row[1],
        'course': row[7],
        'user_id': '',
        'course_id': '',
        'endpoint': '',
        'status': ''
    }

    # Request to users endpoint
    data['endpoint'] = 'users'
    response = request_to_ureditos(
        **{'values[0]': data.get('username'), 'field': 'username', 'wsfunction': 'core_user_get_users_by_field'})
    if response.ok:
        response = response.json()
        response = response[0]
        data['user_id'] = response.get('id')
        # Request to courses endpoint
        data['endpoint'] = 'courses'
        response = request_to_ureditos(
            wsfunction='core_course_get_courses_by_field', value=data.get('course'), field='shortname')
        if response.ok:
            response = response.json()
            response = response['courses'][0]
            data['course_id'] = response.get('id')
            # Request to enroll endpoint
            data['endpoint'] = 'enroll'
            response = request_to_ureditos(**{'wsfunction': 'enrol_manual_enrol_users', 'enrolments[0][roleid]': '5',
                                              'enrolments[0][userid]': str(data.get('user_id')), 'enrolments[0][courseid]': str(data.get('course_id'))})
            if response.ok:
                data['status'] = 'success'
            else:
                data['status'] = 'fail'

        else:
            data['status'] = 'fail'

    else:
        data['status'] = 'fail'

    return data


def requests_for_sms_notifications(row: list, params: dict) -> dict:
    """
    Make the required requests to retrieve data for sms notifications.
    Receives a row from query database results list and params dict as request params.
    Returns a dictionary with data from requests to Ureditos.
    """

    data = {
        'username': row[1],
        'course': row[7],
        'user_id': '',
        'course_id': '',
        'endpoint': '',
        'status': ''
    }

    # Request to users endpoint
    data['endpoint'] = 'users'
    response = request_to_ureditos(
        **{'values[0]': data.get('username'), 'field': 'username', 'wsfunction': 'core_user_get_users_by_field'})
    if response.ok:
        response = response.json()
        response = response[0]
        data['user_id'] = response.get('id')
        # Request to courses endpoint
        data['endpoint'] = 'courses'
        response = request_to_ureditos(
            wsfunction='core_course_get_courses_by_field', value=data.get('course'), field='shortname')
        if response.ok:
            response = response.json()
            response = response['courses'][0]
            data['course_id'] = response.get('id')
            course_fullname = response.get('fullname')
            cellphone_number = str(row[5])

            data['endpoint'] = 'cellphone'
            if cellphone_number.isnumeric() and len(cellphone_number) == 10:
                cellphone_number = f'57{cellphone_number}'
                # cellphone_number = f'573178822671'
                msg = f'Con el fin de mejorar tus competencias, la Universidad Reditos tiene habilitado para ti por quince dias, el curso de {course_fullname}.'
                # Create/update 'recipient' key in params dict
                params['recipient'] = cellphone_number
                # Create/update 'messagedata' key in params dict
                params['messagedata'] = msg

                # Make a request to Masivapp API
                data['endpoint'] = 'masivapp'
                try:
                    response = requests.get(
                        url=URL_API_MASIVAPP, params=params)
                except Exception as e:
                    logging.info(
                        f'Exception in request to MasivApp for user:{data.get("username")} phone:{cellphone_number} exception:{e}')
                    data['status'] = 'fail'
                else:
                    if response.ok:
                        data['status'] = 'success'
                    else:
                        data['status'] = 'fail'
            else:
                data['status'] = 'incorrect'
        else:
            data['status'] = 'fail'
    else:
        data['status'] = 'fail'

    return data


def email_csv_report_writer(row: list, csv_log: str):
    """
    Writes a row in csv report with results of query to DB_NAME database.
    """
    with open(csv_log, mode='a', newline='') as csv_file:
        user_id = str(row[1])
        username = row[2]
        zone = row[3]
        office = row[4]
        course = row[8]

        fields = ['Id', 'Nombre asesor(a)', 'Zona',
                  'Oficina', 'Nombre curso', 'Estado']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fields)

        csv_writer.writerow(
            {'Id': f"CC:{user_id}", 'Nombre asesor(a)': username, 'Zona': zone, 'Oficina': office, 'Nombre curso': course, 'Estado': 'Inscrito'})
