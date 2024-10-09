from pydantic import BaseModel, EmailStr

class ChatQueryModel(BaseModel):
    """
    Model for chatbot query
    """
    query: str