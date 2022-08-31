import requests
from app.config import URL_API_UREDITOS, API_UREDITOS_TOKEN, URL_API_MASIVAPP
import logging


def request_to_ureditos(**kwargs) -> requests.Response:
    """
    Make a request with input arguments as params.
    ### Parameters
    `**kwargs`
        Keyword arguments to include in request as parameters.

    ### Returns
    `requests.Response`
        Response object with format of Universidad Réditos API.

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


def requests_for_enrolling_moodle(username: str, course: str) -> dict:
    """
    Make the required requests to retrieve data and enroll on Universidad Réditos API.
    ### Parameters
    `username: str`
        Username string.
    `course: str`
        Course short name string.

    ### Returns
    `dict`
        Dictionary with data retrived from API requests responses during enrollment process.
    """
    data = {
        'username': username,
        'course': course,
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


def requests_for_sms_notifications(username: str, course: str, cellphone: str, headers: dict, body: dict) -> dict:
    """
    Make the required requests to retrieve data from Universidad Réditos API and send a SMS notification to user by Masivian SMS API.

    ### Parameters
    `username: str`
        Username string.
    `course: str`
        Course short name string.
    `cellphone: str`
        Cellphone string.
    `headers: dict`
        Required headers to make requests to Masivian SMS API. See documentation in https://docs.masivian.com/sms.
    `body: dict`
        Required data format to make requests to Masivian SMS API. See documentation in https://docs.masivian.com/sms.

    ### Returns
    `dict`
        Dictionary with data retrived from API requests responses during SMS notification process.

    """

    data = {
        'username': username,
        'course': course,
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
            cellphone_number = str(cellphone)

            data['endpoint'] = 'cellphone'
            if cellphone_number.isnumeric() and len(cellphone_number) == 10:
                cellphone_number = f'57{cellphone_number}'
                msg = f'Con el fin de mejorar tus competencias, la Universidad Reditos tiene habilitado para ti por quince dias, el curso de {course_fullname}.'
                # Set 'to' body key with user cellphone number.
                body['to'] = cellphone_number
                # Set 'text' body key with text message format.
                body['text'] = msg

                # Make a request to Masivapp API
                data['endpoint'] = 'masivapp'
                try:
                    # response = requests.get(
                    #     url=URL_API_MASIVAPP, params=params)
                    response = requests.post(
                        url=URL_API_MASIVAPP, data=body, headers=headers)
                except Exception:
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
