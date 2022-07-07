from dotenv import load_dotenv
import os

# Execute the load_dotenv() function
load_dotenv()

# Table names
TABLA_CONSOLIDADO = "TblReporteConsolidadoUnicosZona"

# Months dict for locale month name
MONTHS = {
    1: "ENERO",
    2: "FEBRERO",
    3: "MARZO",
    4: "ABRIL",
    5: "MAYO",
    6: "JUNIO",
    7: "JULIO",
    8: "AGOSTO",
    9: "SEPTIEMBRE",
    10: "OCTUBRE",
    11: "NOVIEMBRE",
    12: "DICIEMBRE"
}

# Flask App secret key
SECRET_KEY = os.getenv('SECRET_KEY') or os.environ.get('SECRET_KEY')

# API Ureditos
# URL API Ureditos
URL_API_UREDITOS = os.getenv(
    'URL_API_UREDITOS') or os.environ.get('URL_API_UREDITOS')
# API Ureditos Token
API_UREDITOS_TOKEN = os.getenv(
    'API_UREDITOS_TOKEN') or os.environ.get('API_UREDITOS_TOKEN')

# API Masivapp
# URL API Masivapp
URL_API_MASIVAPP = os.getenv(
    'URL_API_MASIVAPP') or os.environ.get('URL_API_MASIVAPP')
# API Masivapp username
API_MASIVAPP_USERNAME = os.getenv(
    'API_MASIVAPP_USERNAME') or os.environ.get('API_MASIVAPP_USERNAME')
# API Masivapp username
API_MASIVAPP_PASSWORD = os.getenv(
    'API_MASIVAPP_PASSWORD') or os.environ.get('API_MASIVAPP_PASSWORD')

# Azure environment settings
# Connection String
CONNECT_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING') or os.environ.get(
    'AZURE_STORAGE_CONNECTION_STRING')
# Name of File share resource in Azure account
SHARE_NAME = os.getenv(
    'AZURE_FILE_SHARE') or os.environ.get('AZURE_FILE_SHARE')

# Database settings
# Host
DB_HOST = os.getenv("DB_HOST") or os.environ.get("DB_HOST")
# Database name
DB_NAME = os.getenv("DB_NAME") or os.environ.get("DB_NAME")
# Database username
DB_USERNAME = os.getenv("DB_USERNAME") or os.environ.get("DB_USERNAME")
# Database password
DB_PASSWORD = os.getenv("DB_PASSWORD") or os.environ.get("DB_PASSWORD")

# Email settings
# SMTP Host
SMTP_HOST = os.getenv('SMTP_HOST') or os.environ.get('SMTP_HOST')
# SMTP Port
SMTP_PORT = os.getenv('SMTP_PORT') or os.environ.get('SMTP_PORT')
# SMTP Username
SMTP_USERNAME = os.getenv('SMTP_USERNAME') or os.environ.get('SMTP_USERNAME')
# SMTP Password
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD') or os.environ.get('SMTP_PASSWORD')
# Recipients to send email notifications by default
EMAIL_RECIPIENTS = os.getenv(
    'EMAIL_RECIPIENTS') or os.environ.get('EMAIL_RECIPIENTS')
