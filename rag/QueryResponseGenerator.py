import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from rag.AzureSearchContentRetriever import AzureSearchContentRetriever

# Load environment variables
load_dotenv(dotenv_path="../.env")

class QueryResponseGenerator:
    """
    Class to generate responses to user queries using Azure OpenAI and Azure Cognitive Search.
    """

    def __init__(self):
        # Retrieve environment variables for Azure OpenAI
        self.model_name = os.getenv("AZURE_OPENAI_GPT4_MODEL")
        #print("model_name", self.model_name)
        self.deployment = os.getenv("AZURE_OPENAI_GPT4_DEPLOYMENT")
        #print("deployment", self.deployment)
        self.api_key = os.getenv("AZURE_OPENAI_GPT4_KEY")
        self.endpoint = os.getenv("AZURE_OPENAI_GPT4_ENDPOINT")
        self.version = os.getenv("AZURE_OPENAI_GPT4_VERSION")
        self.temperature = 0.2
        self.llm = self._initialize_llm_instance()
        self.retriever = AzureSearchContentRetriever()

    def _initialize_llm_instance(self) -> AzureChatOpenAI:
        """
        Initialize an instance of AzureChatOpenAI with the provided configuration.
        """
        return AzureChatOpenAI(
            model=self.model_name,
            azure_deployment=self.deployment,
            openai_api_version=self.version,
            openai_api_key=self.api_key,
            azure_endpoint=self.endpoint,
            temperature=self.temperature
        )

    def get_chat_query_response(self, query: str) -> str:
        """
        Generate a response to a user query using the provided query and context.
        """
        # Retrieve relevant documents using the DocumentRetriever
        retrieved_documents = self.retriever.retrieve_searched_documents(query)
        

        # If no documents are found, return a no results message
        if not retrieved_documents:
            return "No relevant documents found."

        # Create a prompt template
        template = (
            '''
            You are a highly intelligent question-answer bot. You are designed to provide comprehensive and informative responses 
            based on the context of the provided documents. You should answer the user's questions and offer guidance 
            as an experienced HR professional would, considering policies, procedures, and best practices mentioned in the handbook.
            If the question is not directly related to the context or you do not have enough information to answer it accurately, 
            respond with 'I'm not sure how to answer that based on the provided information.' or 'I don't have the information to answer this question.' 
            Be concise with your answer and complete the sentences. Do not leave anything incomplete.

            Context: {context}

            Question: {query}
            '''
        )
        prompt_template = ChatPromptTemplate.from_template(template)

        # Format the prompt with the retrieved documents and the user query
        formatted_prompt = prompt_template.format_prompt(context=retrieved_documents, query=query)

        # Convert the formatted prompt to messages
        messages = formatted_prompt.to_messages()

        # Get the response from AzureChatOpenAI
        get_llm_response = self.llm(messages)

        # Extract the content from the response and return it
        response_content = get_llm_response.content
        return response_content


if __name__ == "__main__":
    content_generation_object = QueryResponseGenerator()
    # query to retrieve documents
    response = content_generation_object.get_chat_query_response("When does the AppleCare Protection Plan's coverage for defects begin?")
    print("Response is:\n", response)

