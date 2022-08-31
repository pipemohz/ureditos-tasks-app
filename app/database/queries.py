import pyodbc
import os
from app.config import DB_HOST, DB_NAME, DB_USERNAME, DB_PASSWORD


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
