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
    Sends an email with content of message MIMEMultipart object.
    ### Parameters
    `message: MIMEMultipart`
        An object of MIMEMultipart class. The function uses message['To'] value as the recipients to send email and message['From'] value as the sender.
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


def set_email_format(text: str, recipients=None, filename=None) -> MIMEMultipart:
    """
    Sets format of an RFC email message with `recipients` and `EMAIL_RECIPIENTS` as recipients, `text` as text message and inserting the file specified by `filename` as attachment.
    If `recipients` is `None`, the message will only include the recipients in environment variable `EMAIL_RECIPIENTS`.
    If `filename` is `None`, no file will be inserted as an attachment. 

    ### Parameters
    `text: str`
        Text of message.
    `recipients: list | None`
        List of recipients to send message.
    `filename: str | None`
        Path to the file to attach in message.

    ### Returns
    `MIMEMultipart`
        MIMEMultipart object which represents a RFC formatted email message.
    """
    msg = MIMEMultipart()

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


def send_email_to(recipients: list, filename: str, text=EMAIL_TEXT_SERVICIO):
    """
    Sends an email message with `recipients` and EMAIL_RECIPIENTS as recipients and inserting the file specified by `filename` as attachment.

    ### Parameters
    `recipients: list`
        List of recipients to send email.
    `filename: str`
        Path to the file to attach to email message.
    `text: str`
        Text of email message. By default, text = EMAIL_TEXT_SERVICIO.

    """
    message = set_email_format(text, recipients, filename)
    send_email(message)
