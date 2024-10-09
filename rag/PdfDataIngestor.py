import os
from dotenv import load_dotenv
from langchain_openai import AzureOpenAIEmbeddings
from langchain.vectorstores.azuresearch import AzureSearch
from rag.PdfDataExtractor import PDFExtractor
from azure.storage.blob import BlobServiceClient
import tempfile

class DataIngestor:

    def __init__(self):
        load_dotenv(dotenv_path='../.env')
        
        self.endpoint = os.environ["AZURE_SEARCH_ENDPOINT"]
        self.key_credential = os.environ["AZURE_SEARCH_KEY"] 
        self.index_name = os.environ["AZURE_SEARCH_INDEX"]
        self.azure_openai_endpoint = os.environ["AZURE_OPENAI_EMBEDDING_ENDPOINT"]
        self.azure_openai_key = os.environ["AZURE_OPENAI_EMBEDDING_KEY"] 
        self.azure_openai_embedding_deployment = os.environ["AZURE_OPENAI_EMBEDDING_DEPLOYMENT"]
        self.azure_openai_api_version = os.environ["AZURE_OPENAI_EMBEDDING_VERSION"]
        self.azure_storage_connection_string = os.environ.get("AZURE_STORAGE_CONNECTION")
        self.blob_container_name = os.environ.get("AZURE_BLOB_CONTAINER")
        
        print("blob_container_name",self.blob_container_name)
        
        self.embeddings = AzureOpenAIEmbeddings(
            azure_deployment=self.azure_openai_embedding_deployment,
            openai_api_version=self.azure_openai_api_version,
            azure_endpoint=self.azure_openai_endpoint,
            api_key=self.azure_openai_key
        )

        self.vector_store = AzureSearch(
            azure_search_endpoint=self.endpoint,
            azure_search_key=self.key_credential,
            index_name=self.index_name,
            embedding_function=self.embeddings.embed_query,
            semantic_configuration_name="default"
        )

    def ingest_data(self, blob_name):
        blob_service_client = BlobServiceClient.from_connection_string(self.azure_storage_connection_string)
        blob_client = blob_service_client.get_blob_client(container=self.blob_container_name, blob=blob_name)

        # Download the blob content to memory
        download_stream = blob_client.download_blob()
        file_content = download_stream.readall()  # Read content into memory

        # Create a temporary file to use with PyPDFLoader
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(file_content)
            temp_pdf_path = temp_pdf.name

        # Pass the temporary file path to PDFExtractor
        extractor = PDFExtractor(temp_pdf_path)
        file_chunks = extractor.extract_content()

        # Remove the temporary file after extraction
        os.remove(temp_pdf_path)

        try:
            results = self.vector_store.add_documents(documents=file_chunks)
            return results
        except Exception as e:
            print(f"Data ingestion failed: {e}")


# if __name__ == "__main__":
#     data_ingestor = DataIngestor()
 
#     # Specify the name of the blob you want to ingest
#     blob_name = "AppleCare_ara_NA_en_v3.0.pdf"
 
#     try:
#         result = data_ingestor.ingest_data(blob_name)
#         print("Ingestion result:", result)
#     except Exception as e:
#         print(f"An error occurred: {e}")


























# import os
# import logging
# from dotenv import load_dotenv
# from azure.identity import DefaultAzureCredential
# from langchain_openai import AzureOpenAIEmbeddings
# from azure.identity import get_bearer_token_provider
# from langchain.vectorstores.azuresearch import AzureSearch
# from rag_backend.DataExtractor import PDFExtractor
# from azure.storage.blob import BlobServiceClient
# import tempfile

# class DataIngestor:
#     """
#     A class to handle data ingestion into Azure Search.

#     Attributes:
#     ----------
#     None

#     Methods:
#     -------
#     ingest_data(file_chunks):
#         Ingests the provided file chunks into Azure Search.
#     """

#     def __init__(self):
#         load_dotenv(dotenv_path='../.env')

#         try:
#             self.endpoint = os.environ["AZURE_AI_SEARCH_API_ENDPOINT"]
#             self.key_credential = os.environ["AZURE_AI_SEARCH_API_KEY"] if len(os.environ["AZURE_AI_SEARCH_API_KEY"]) > 0 else None
#             self.index_name = os.environ["AZURE_AI_SEARCH_INDEX"]
#             self.azure_openai_endpoint = os.environ["AZURE_EMBEDDING_OPENAI_ENDPOINT"]
#             self.azure_openai_key = os.environ["AZURE_EMBEDDING_OPENAI_API_KEY"] if len(os.environ["AZURE_EMBEDDING_OPENAI_API_KEY"]) > 0 else None
#             self.azure_openai_embedding_deployment = os.environ["AZURE_EMBEDDING_DEPLOYMENT"]
#             self.azure_openai_api_version = os.environ["AZURE_EMBEDDING_OPENAI_API_VERSION"]
#             self.azure_storage_connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
#             self.blob_container_name = os.environ.get("BLOB_CONTAINER_NAME")
            
#         except KeyError as e:
#             logging.error(f"Environment variable {e} not found.")
#             raise

#         credential = self.key_credential or DefaultAzureCredential()

#         openai_credential = DefaultAzureCredential()
#         token_provider = get_bearer_token_provider(openai_credential, "https://cognitiveservices.azure.com/.default")

#         self.embeddings = AzureOpenAIEmbeddings(
#             azure_deployment=self.azure_openai_embedding_deployment,
#             openai_api_version=self.azure_openai_api_version,
#             azure_endpoint=self.azure_openai_endpoint,
#             api_key=self.azure_openai_key,
#             azure_ad_token_provider=token_provider if not self.azure_openai_key else None
#         )

#         self.vector_store = AzureSearch(
#             azure_search_endpoint=self.endpoint,
#             azure_search_key=self.key_credential,
#             index_name=self.index_name,
#             embedding_function=self.embeddings.embed_query,
#             semantic_configuration_name="default"
#         )

#     def ingest_data(self, blob_name):
#         """
#         Ingests the provided file chunks into Azure Search.

#         Parameters:
#         ----------
#         blob_name : str
#             The name of the blob to be ingested.

#         Returns:
#         -------
#         dict
#             The result of the ingestion process.
#         """
#         blob_service_client = BlobServiceClient.from_connection_string(self.azure_storage_connection_string)
#         blob_client = blob_service_client.get_blob_client(container=self.blob_container_name, blob=blob_name)

#         # Download the blob content to memory
#         download_stream = blob_client.download_blob()
#         file_content = download_stream.readall()  # Read content into memory

#         # Create a temporary file to use with PyPDFLoader
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
#             temp_pdf.write(file_content)
#             temp_pdf_path = temp_pdf.name

#         # Pass the temporary file path to PDFExtractor
#         extractor = PDFExtractor(temp_pdf_path)
#         file_chunks = extractor.extract_content()

#         # Remove the temporary file after extraction
#         os.remove(temp_pdf_path)

#         try:
#             results = self.vector_store.add_documents(documents=file_chunks)
#             logging.info("Data ingestion successful.")
#             return results
#         except Exception as e:
#             logging.error(f"Data ingestion failed: {e}")
#             raise