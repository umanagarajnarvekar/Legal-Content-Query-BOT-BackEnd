import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

class BlobStorageDatabase:
    """
    Class for interacting with an Azure Blob Storage database.

    This class provides functionality to upload files to an Azure Blob Storage container.
    It uses environment variables to retrieve the connection string and container name.

    Attributes:
        azure_storage_connection_string (str): The connection string for the Azure Blob Storage account.
        blob_container_name (str): The name of the Azure Blob Storage container to upload files to.
        blob_service_client (BlobServiceClient): The BlobServiceClient instance used to interact with Azure Blob Storage.

    Methods:
        upload_file(file): Uploads the given file to the specified blob container.
    """

    def __init__(self):
        """
        Initializes a BlobStorageDatabase instance using environment variables for the connection string and container name.

        Retrieves:
            - AZURE_STORAGE_CONNECTION: Azure Blob Storage connection string.
            - AZURE_BLOB_CONTAINER: Name of the blob container to upload files.

        Sets up:
            - A BlobServiceClient instance to interact with Azure Blob Storage.
        """
        self.azure_storage_connection_string = os.environ.get("AZURE_STORAGE_CONNECTION")
        self.blob_container_name = os.environ.get("AZURE_BLOB_CONTAINER")
        self.blob_service_client = BlobServiceClient.from_connection_string(self.azure_storage_connection_string)

    def upload_file(self, file):
        """
        Uploads a file to the Azure Blob Storage container specified in the environment variables.

        Args:
            file : The file to be uploaded. Should be opened in binary mode.

        Returns:
            dict: A dictionary containing a status code and a message. 
                  - If the upload is successful, the status code is 200, and the message indicates success.
                  - If an error occurs during the upload, the status code is 400, and the message describes the error.
        
        Raises:
            Exception: Any exception encountered during the file upload is caught and returned with an error message.

        Example:
            result = blob_storage.upload_file(open("document.pdf", "rb"))
            print(result["message"])  # "Legal document PDF uploaded successfully" or an error message.
        """
        blob_client = self.blob_service_client.get_blob_client(container=self.blob_container_name, blob=file.name)

        try:
            blob_client.upload_blob(file)

        except Exception as e:
            return {
                "status_code": 400,
                "message": f"File upload failed: {str(e)}"
            }
        finally:
            file.close()

        return {
            "status_code": 200,
            "message": "Legal document PDF uploaded successfully"
        }
