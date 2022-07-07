# ureditos-tasks-app
App for enrolling consultants in universidad Réditos moodle platform, sending SMS notifications to enrolled consultants and sending email reports to organization coordinators. It is based on Azure functions technology with python's Flask Framework.

## Installation 🔧

Clone the repository in a your work folder.

## Configuration

### Download all packages required

pip install -r requirements.txt

### Create an environment file

You must create a .env file for project configuration. It must contain following variables:

##################
# Flask settings #
##################

# Flask app secret key
SECRET_KEY=U5MrSqJbV8Nlwn8Qu6JqDW9NJ9lSB9hN

#########################
# API Ureditos settings #
#########################

# URL API Ureditos
URL_API_UREDITOS=https://www.universidadreditos.com/webservice/rest/server.php

# Access token of API Ureditos
API_UREDITOS_TOKEN=your_access_token

#########################
# API Masivapp settings #
#########################

# URL API Masivapp (SMS)
URL_API_MASIVAPP=https://api-sms.masivapp.com/SmsHandlers/sendhandler.ashx
# API Masivapp username
API_MASIVAPP_USERNAME=your_masivapp_username
# API Masivapp password
API_MASIVAPP_PASSWORD=your_masivapp_password

##################
# Email settings #
##################

SMTP_HOST = smtp_server_domain
SMTP_PORT = smtp_port
SMTP_USERNAME = email_username
SMTP_PASSWORD = email_password

# List of email recipients to send notifications.
EMAIL_RECIPIENTS=mail1@example.com,mail2@example.com

#####################
# Database settings #
#####################

DB_HOST=database_server
DB_NAME=database_name
DB_USERNAME=database_usernae
DB_PASSWORD=database_password

##################
# Azure settings #
##################
AZURE_FILE_SHARE=azure_file_share_folder
AZURE_STORAGE_CONNECTION_STRING="your_azure_storage_connection_string"


