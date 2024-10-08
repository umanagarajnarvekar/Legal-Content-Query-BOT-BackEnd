import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

# Load environment variables
load_dotenv(dotenv_path="../.env")

class AzureSearchContentRetriever:     
    def __init__(self):
        self.azure_api_key = os.getenv("AZURE_SEARCH_KEY")
        self.azure_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        self.azure_index_name = os.getenv("AZURE_SEARCH_INDEX")
        self.top_results = int(os.getenv("AZURE_SEARCH_TOP_RESULTS", "10"))  # Default to 10 if not set

        #print(f"Azure API Key: {self.azure_api_key[:5]}..." if self.azure_api_key else "Not set")
        #print(f"Azure Endpoint: {self.azure_endpoint}")
        #print(f"Azure Index Name: {self.azure_index_name}")
        #print(f"Top Results: {self.top_results}")

        if not all([self.azure_api_key, self.azure_endpoint, self.azure_index_name]):
            raise ValueError("Missing required environment variables")

        # Print the full search URL
        full_search_url = f"{self.azure_endpoint}/indexes/{self.azure_index_name}/docs/search?api-version=2023-07-01-Preview"
        #print(f"Full Search URL: {full_search_url}")

        self.search_client = self._initialize_search_query_client()

    def _initialize_search_query_client(self) -> SearchClient:
        try:
            return SearchClient(self.azure_endpoint, self.azure_index_name, AzureKeyCredential(self.azure_api_key))
        except Exception as e:
            print(f"Error initializing SearchClient: {str(e)}")
            #raise

    def retrieve_searched_documents(self, query: str) -> str:
        try:
            results = self.search_client.search(query, top=self.top_results)
            retrieved_documents = []

            for result in results:
                print("Result:", result)
                if 'chunk' in result:
                    retrieved_documents.append(result['chunk'])
                elif 'content' in result:
                    retrieved_documents.append(result['content'])
            
            combined_documents = "\n".join(retrieved_documents)
            return combined_documents
        except Exception as e:
            print(f"Error during search: {str(e)}")
            #raise

'''if __name__ == "__main__":
    try:
        content_retriever_object = AzureSearchContentRetriever()
        response = content_retriever_object.retrieve_searched_documents("What does the AppleCare Protection Plan for iPhone cover?")
        print("Response:", response)
    except Exception as e:
        print(f"An error occurred: {str(e)}")'''