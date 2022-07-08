import logging
from azure.core.exceptions import (
    ResourceExistsError,
    ResourceNotFoundError
)

from azure.storage.fileshare import (
    ShareServiceClient,
    ShareClient,
    ShareDirectoryClient,
    ShareFileClient
)


def upload_local_file(connection_string: str, local_file_path: str, share_name: str, dest_file_path: str):
    """
    Uploads the file specified by local_file_path to Azure's file share resource with name share_name.
    A connection_string is required to stablish a connection with  an Azure file share resource through a ShareFileClient object.
    The dest_file_path argument must point to an existing folder in file share. Otherwise an exception will be throw.
    For more details see the Azure documentation: https://docs.microsoft.com/en-us/azure/storage/files/storage-python-how-to-use-file-storage?tabs=python.
    """
    try:
        source_file = open(local_file_path, "rb")
        data = source_file.read()

        # Create a ShareFileClient from a connection string
        file_client = ShareFileClient.from_connection_string(
            connection_string, share_name, dest_file_path)

        logging.info(f"Uploading to: {share_name}/{dest_file_path}")
        file_client.upload_file(data)

    except ResourceExistsError as ex:
        logging.info(f"ResourceExistsError: {ex.message}")

    except ResourceNotFoundError as ex:
        logging.info(f"ResourceNotFoundError: {ex.message}")
