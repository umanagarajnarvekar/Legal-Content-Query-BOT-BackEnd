from pydantic import BaseModel

class ChatQueryModel(BaseModel):
    """
    This model is used to validate and structure the data for a chatbot query.
    It ensures that the query input is a valid string and conforms to the expected structure.

    Attributes:
        query (str): The user's query that will be processed by the chatbot.

    Example:
        query_data = ChatQueryModel(query="question")

    Raises:
        ValidationError: If the input data does not conform to the required schema.
    """
    
    query: str
