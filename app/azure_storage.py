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


def upload_local_file(connection_string, local_file_path, share_name, dest_file_path):
    try:
        source_file = open(local_file_path, "rb")
        data = source_file.read()

        # Create a ShareFileClient from a connection string
        file_client = ShareFileClient.from_connection_string(
            connection_string, share_name, dest_file_path)

        logging.info(f"Uploading to: {share_name}/{dest_file_path}")
        file_client.upload_file(data)

    except ResourceExistsError as ex:
        logging.info("ResourceExistsError: {ex.message}")

    except ResourceNotFoundError as ex:
        logging.info("ResourceNotFoundError: {ex.message}")
