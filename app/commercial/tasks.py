import tempfile
from datetime import datetime
from os.path import join
import csv
import logging
from app.email import send_email_to
from concurrent.futures import ThreadPoolExecutor
import concurrent
from app.azure_storage import upload_local_file
from app.config import *
from app.database import query_database
from app.api import requests_for_enrolling_moodle, requests_for_sms_notifications
from app.files import email_csv_report_writer


def enrolling_moodle():
    """
    Executes the enrollment of users in Moodle courses by results of a query to database DB_NAME.
    """
    # Today's date
    today = datetime.now()

    # Today's month
    # month = MONTHS.get(today.month)
    # FIXME Delete line below and uncomment the up one.
    month = MONTHS.get(7)

    # Definition of tempdir path.
    folder = tempfile.gettempdir()

    # Build query to database
    query = f"SELECT * FROM {TABLA_INDICADORES_COMERCIALES} WHERE Ejecucion = '{month}-{today.year}' ORDER BY Zona"

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
                requests_for_enrolling_moodle, row[1], row[6]) for row in query_results]

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
        'comerciales', 'logsMoodle', f'logMoodle{today.strftime("%Y-%m-%d-%H")}h.csv'))
    # Execute uploading function for creating a log on file share resource
    upload_local_file(CONNECT_STRING, txt_log,
                      SHARE_NAME, 'logMoodleAcciones.txt')


def send_sms_notifications():
    """
    Executes the SMS notifications module which sends a SMS message to each user for every course enrolled.
    """
    # Today's date
    today = datetime.now()

    # Today's month
    # month = MONTHS.get(today.month)
    # FIXME Delete line below and uncomment the up one.
    month = MONTHS.get(7)

    # Definition of tempdir path.
    folder = tempfile.gettempdir()

    # Build query to database
    query = f"SELECT * FROM {TABLA_INDICADORES_COMERCIALES} WHERE Ejecucion = '{month}-{today.year}' ORDER BY Zona"

    # Make query to database
    query_results = query_database(query)

    # Definition of csv and txt file paths.
    csv_log = join(folder, f'logAvisosSMS{today.strftime("%Y-%m-%d-%H")}h.csv')
    txt_log = join(folder, 'logMoodleAcciones.txt')

    # Declare a dict header to attach Masivian SMS API required request headers (https://docs.masivian.com/sms).
    headers = {
        'Authorization': 'Basic Token',
    }

    # Declare a dict body to send data to Masivian SMS API (https://docs.masivian.com/sms).
    body = {
        "isPremium": False,
        "isFlash": False,
        "isLongmessage": False,
        "isRandomRoute": False,
    }

    with open(csv_log, mode='w', newline='') as csv_file, open(txt_log, mode='a') as txt:
        fields = ['username', 'user_id',
                  'course', 'course_id', 'status']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fields)
        csv_writer.writeheader()
        txt.write(f'[{datetime.now()}] Inicio proceso de SMS.\n')

        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = [executor.submit(
                requests_for_sms_notifications, row[1], row[6], row[5], headers, body) for row in query_results]
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
        'comerciales', 'logsSMS', f'logAvisosSMS{today.strftime("%Y-%m-%d-%H")}h.csv'))
    # Execute uploading function for creating a log on file share resource
    upload_local_file(CONNECT_STRING, txt_log,
                      SHARE_NAME, 'logMoodleAcciones.txt')


def send_email_notifications():
    """
    Executes the email notifications module which sends a report by email of all users enrolled to each zone coordinator and recipients in EMAIL_RECIPIENTS.
    """
    # Today's date
    today = datetime.now()

    # Today's month
    # month = MONTHS.get(today.month)
    # FIXME Delete line below and uncomment the up one.
    month = MONTHS.get(7)

    # Definition of tempdir path.
    folder = tempfile.gettempdir()

    # # Build query to TABLA_CONSOLIDADO and order by Zona
    query = f"SELECT * FROM {TABLA_INDICADORES_COMERCIALES} WHERE Ejecucion = '{month}-{today.year}' ORDER BY Zona"

    # Make query to database
    query_results = query_database(query)

    # Build query to TABLA_CONSOLIDADO for getting email recipients
    query = f"SELECT DISTINCT CorreoElectronico FROM {TABLA_INDICADORES_COMERCIALES}"

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
                email_csv_report_writer, str(row[1]), row[2], row[3], row[4], row[7], csv_log) for row in query_results]

        # Execute function for sending email to all coordinators.
        send_email_to(recipients, csv_log, text=EMAIL_TEXT_COMERCIALES)
        txt.write(f'[{datetime.now()}] Fin proceso de correos.\n')

    # Execute uploading function for creating a csv log on file share resource
    upload_local_file(CONNECT_STRING, csv_log, SHARE_NAME, join(
        'comerciales', 'logsCorreo', f'UReditos_Consolidado_Inscripciones {today.strftime("%Y-%m-%d")}.csv'))
    # Execute uploading function for creating a log on file share resource
    upload_local_file(CONNECT_STRING, txt_log,
                      SHARE_NAME, 'logMoodleAcciones.txt')
