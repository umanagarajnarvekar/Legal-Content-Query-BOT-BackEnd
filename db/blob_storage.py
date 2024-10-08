import os
from azure.storage.blob import BlobServiceClient


from dotenv import load_dotenv

load_dotenv()

class BlobStorageDatabase:
    '''
    Class to interact with the database
    '''

    def __init__(self):
        self.azure_storage_connection_string = os.environ.get("AZURE_STORAGE_CONNECTION")
        self.blob_container_name = os.environ.get("AZURE_BLOB_CONTAINER")
        self.blob_service_client = BlobServiceClient.from_connection_string(self.azure_storage_connection_string)
        
    def upload_file(self, file):
        blob_client = self.blob_service_client.get_blob_client(container=self.blob_container_name, blob=file)

        try:
            blob_client.upload_blob(file)

        except Exception as e:
            return {"status_code":400,
                    "message": f"File upload failed: {str(e)}"}
        finally:
            file.close()
        return {
            "status_code":200,
            "message": "Legal document PDF uploaded successfully"}