import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

# Load environment variables from the specified .env file
load_dotenv(dotenv_path="../.env")

class AzureSearchContentRetriever:
    """
    A class to interact with Azure Cognitive Search and retrieve documents from a specified index.
    It initializes the search client with credentials from environment variables and provides a method
    to perform the search query and return the results.
    """
    
    def __init__(self):
        """
        Initializes the AzureSearchContentRetriever by loading environment variables and setting up
        the necessary credentials and search configurations.
        """
        # Load Azure Search API key, endpoint, and index name from environment variables
        self.azure_api_key = os.getenv("AZURE_SEARCH_KEY")
        self.azure_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        self.azure_index_name = os.getenv("AZURE_SEARCH_INDEX")
        # Optionally load top results limit, default to 10 if not set in .env file
        self.top_results = int(os.getenv("AZURE_SEARCH_TOP_RESULTS", "10"))

        # Check if all necessary environment variables are set, raise an error if not
        if not all([self.azure_api_key, self.azure_endpoint, self.azure_index_name]):
            raise ValueError("Missing required environment variables: Ensure AZURE_SEARCH_KEY, AZURE_SEARCH_ENDPOINT, and AZURE_SEARCH_INDEX are set.")
        
        # Debugging: Full search URL for reference (optional to print)
        full_search_url = f"{self.azure_endpoint}/indexes/{self.azure_index_name}/docs/search?api-version=2023-07-01-Preview"
        #print(f"Full Search URL: {full_search_url}")

        # Initialize the search client
        self.search_client = self._initialize_search_query_client()

    def _initialize_search_query_client(self) -> SearchClient:
        """
        Initializes and returns the SearchClient object to interact with the Azure Search service.
        
        Returns:
            SearchClient: The initialized client used to execute search queries.
        """
        try:
            # Return a SearchClient with the specified endpoint, index name, and API key credential
            return SearchClient(self.azure_endpoint, self.azure_index_name, AzureKeyCredential(self.azure_api_key))
        except Exception as e:
            # Handle any errors in initializing the SearchClient
            print(f"Error initializing SearchClient: {str(e)}")
            #raise

    def retrieve_searched_documents(self, query: str) -> str:
        """
        Executes the search query against the Azure search index and retrieves the relevant documents.
        
        Args:
            query (str): The search term or query to search in the Azure index.
        
        Returns:
            str: A concatenated string of the retrieved document contents.
        """
        try:
            # Execute the search query with the given query string, limiting results by top_results
            results = self.search_client.search(query, top=self.top_results)
            retrieved_documents = []  # To store the content of each result

            # Iterate through the search results
            for result in results:
                print("Result:", result)  # Debugging: Print each result (optional)
                
                # Append the 'chunk' field if available, else 'content' field
                if 'chunk' in result:
                    retrieved_documents.append(result['chunk'])
                elif 'content' in result:
                    retrieved_documents.append(result['content'])
            
            # Combine all retrieved document contents into a single string
            combined_documents = "\n".join(retrieved_documents)
            return combined_documents
        except Exception as e:
            # Handle any errors during the search process
            print(f"Error during search: {str(e)}")
            #raise

# Example usage (commented out):
'''
if __name__ == "__main__":
    try:
        # Create an instance of AzureSearchContentRetriever
        content_retriever_object = AzureSearchContentRetriever()
        # Search for a specific query
        response = content_retriever_object.retrieve_searched_documents("What does the AppleCare Protection Plan for iPhone cover?")
        # Print the search response
        print("Response:", response)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
'''
