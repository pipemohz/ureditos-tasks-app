import logging
import smtplib
from os.path import basename
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from .config import *


def send_email(message: MIMEMultipart):
    """
    Sends an email to message['To'] recipients value with content of message MIMEMultipart argument.
    """
    try:
        with smtplib.SMTP(host=SMTP_HOST, port=SMTP_PORT, timeout=10) as conn:
            conn.starttls()
            conn.login(user=SMTP_USERNAME,
                       password=SMTP_PASSWORD)
            conn.sendmail(from_addr=message.get('From'), to_addrs=message.get(
                'To').split(','), msg=message.as_string())
    except Exception as e:
        logging.info(
            f'The following exception has ocurred during sending email notifications: {e}')
    else:
        logging.info('The email notifications were sent successfully.')


def set_email_format(recipients=None, filename=None) -> MIMEMultipart:
    """
    Sets format of an e-mail message with the recipients and EMAIL_RECIPIENTS as recipients and inserting the file specified by filename as attachment.
    If recipients is None, the message will only include the recipients in environment variable EMAIL_RECIPIENTS.
    If filename is None, no file will be inserted as an attachment. 
    """
    msg = MIMEMultipart()
    text = """Buen día, equipo de coordinador@s regionales. Les estamos enviando la información de las asesoras matriculadas en los cursos de la Universidad Réditos, de acuerdo con los resultados en los indicadores de nivel de servicio del último bimestre. Incluimos información detallada para que puedan realizar la gestión correspondiente. Contamos contigo para movilizarlos y juntos continuemos potencializando sus competencias.
    
    Importante: en el archivo adjunto podrán filtrar la Zona para que puedan observar sus asesoras.

    Adicionalmente, les compartimos a continuación un link del tablero que contiene el detalle de los indicadores por asesora:

    https://app.powerbi.com/links/qIoXgLdInx?ctid=d6a2ecba-dd2a-4f0c-a632-6798e31995bb&pbi_source=linkShare&bookmarkGuid=a76f592e-47c5-4da3-ba1a-a5e70c69369a
    
    Nota: En el tablero pueden seleccionar la pestaña "HV Vendedor" y luego pueden buscar la cédula de cada colaborador para ver el resultado de sus indicadores. El filtro de fecha debe tener seleccionado el Año-Mes que desean consultar.
    
    En la Universidad Réditos contamos contigo para que juntos disfrutemos aprendiendo."""

    # Setting of the email message
    msg_to = EMAIL_RECIPIENTS.split(',')
    if recipients:
        msg_to += recipients

    msg['From'] = SMTP_USERNAME
    msg['To'] = ",".join(msg_to)
    msg['Subject'] = "Reporte de asesores matriculados."

    if filename:

        attachment = MIMEBase("application", "octect-stream")

        # attachment_path = join(dirname(__file__), 'Logs', filename)
        with open(filename, mode='rb') as part:
            attachment.set_payload(part.read())

        encoders.encode_base64(attachment)

        attachment.add_header("content-Disposition",
                              'attachment', filename=basename(filename))

        msg.attach(attachment)
        # add in the message body
        msg.attach(MIMEText(text, 'plain'))

    return msg


def send_email_to(recipients: list, filename: str):
    """
    Sends an e-mail message with the recipients arguments and EMAIL_RECIPIENTS as recipients and inserting the file specified by filename as attachment.
    """
    message = set_email_format(recipients, filename)
    send_email(message)
