import requests
from .config import URL_API_UREDITOS, API_UREDITOS_TOKEN


def is_server_up() -> bool:
    """
    Executes a connection test on URL_API_REDITOS. If the server is up returns True, else returns False.
    """
    course_name = 'winner'

    params = {
        'wstoken': API_UREDITOS_TOKEN,
        'wsfunction': 'core_course_get_courses_by_field',
        'moodlewsrestformat': 'json',
        'value': course_name,
        'field': 'shortname',
    }

    try:
        requests.get(url=URL_API_UREDITOS, params=params)
    except requests.RequestException:
        return False
    else:
        return True
