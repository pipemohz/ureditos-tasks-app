from dotenv import load_dotenv
import os

# Execute the load_dotenv() function
load_dotenv()

# Table names
TABLA_INDICADORES_SERVICIO = "TblReporteConsolidadoUnicosZona"
TABLA_INDICADORES_COMERCIALES = "TblReporteConsolidadoUreditosFase2"

# Email text templates
EMAIL_TEXT_SERVICIO = """Buen día, equipo de coordinador@s regionales. Les estamos enviando la información de las asesoras matriculadas en los cursos de la Universidad Réditos, de acuerdo con los resultados en los indicadores de nivel de servicio del último bimestre. Incluimos información detallada para que puedan realizar la gestión correspondiente. Contamos contigo para movilizarlos y juntos continuemos potencializando sus competencias.
    
    Importante: en el archivo adjunto podrán filtrar la Zona para que puedan observar sus asesoras.

    Adicionalmente, les compartimos a continuación un link del tablero que contiene el detalle de los indicadores por asesora:

    https://app.powerbi.com/links/qIoXgLdInx?ctid=d6a2ecba-dd2a-4f0c-a632-6798e31995bb&pbi_source=linkShare&bookmarkGuid=a76f592e-47c5-4da3-ba1a-a5e70c69369a
    
    Nota: En el tablero pueden seleccionar la pestaña "HV Vendedor" y luego pueden buscar la cédula de cada colaborador para ver el resultado de sus indicadores. El filtro de fecha debe tener seleccionado el Año-Mes que desean consultar.
    
    En la Universidad Réditos contamos contigo para que juntos disfrutemos aprendiendo."""

EMAIL_TEXT_COMERCIALES = """Buen día, equipo de coordinador@s regionales. Les estamos enviando la información de las asesoras matriculadas en los cursos de la Universidad Réditos, de acuerdo con sus resultados en los Indicadores Comerciales del último mes. Incluimos información detallada para que puedan realizar la gestión correspondiente. Contamos contigo para movilizarlos y juntos continuemos potencializando sus competencias.
    
    Importante: en el archivo adjunto podrán filtrar la Zona para que puedan observar sus asesoras.

    Adicionalmente, les recordamos que en los tableros de Termómetro podrán consultar el detalle de los indicadores comerciales por asesora.
    
    En la Universidad Réditos contamos contigo para que juntos disfrutemos aprendiendo."""

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
