# ureditos-tasks-app
App for enrolling consultants in universidad Réditos moodle platform, sending SMS notifications to enrolled consultants and sending email reports to organization coordinators. It is based on Azure functions technology with python's Flask Framework.

## Installation 🔧

Clone the repository in a your work folder.

## Configuration

### Prerequisites

* Azure account with active suscription.
* [Azure Functions Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=v4%2Cwindows%2Ccsharp%2Cportal%2Cbash) 4.x.
* If you are going to use Vscode to manage Azure Functions, you will need [The Azure Functions extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions).
* If you are going to use command line to manage Azure Funcions, you will need one of the following tools:
  * [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) version 2.4 or later.
  * The Azure Az [PowerShell module](https://docs.microsoft.com/en-us/powershell/azure/install-az-ps) version 5.9.0 or later.
* A python version supported by Azure Functions. See details [here](https://docs.microsoft.com/en-us/azure/azure-functions/supported-languages#languages-by-runtime-version).

### Create a virtual environment
```
python -m venv .venv
```
### Activate virtul environment

#### Windows
```
.venv\Scripts\activate
```
#### Linux
```
source .venv/bin/activate
```
### Download all packages required
```
pip install -r requirements.txt
```
### Create an environment file

You must create a .env file for project configuration. It must contain following variables:

```
##################
# Flask settings #
##################

# Flask app secret key
SECRET_KEY=your_app_secret_key

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
SMTP_USERNAME = your_email_username
SMTP_PASSWORD = your_email_password

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
AZURE_FILE_SHARE=your_azure_file_share_folder
AZURE_STORAGE_CONNECTION_STRING="your_azure_storage_connection_string"

```

## Running tests
### Open a terminal and check Azure Functions Core Tools is installed
```
func
```
### Start Azure Function
```
func start
```


