import os
from fastapi import FastAPI, File, UploadFile, Request
import psycopg2
from dotenv import load_dotenv
from models.RegistrationModel import RegistrationModel
from models.Login import Login
from models.ChatQueryModel import ChatQueryModel
from db.blob_storage import BlobStorageDatabase
from rag.QueryResponseGenerator import QueryResponseGenerator
# from rag.PdfDataIngestor import DataIngestor #final testing pending to create index via api

app = FastAPI()
load_dotenv()

# Load Azure Blob container environment variable
AZURE_BLOB_CONTAINER = os.environ.get("AZURE_BLOB_CONTAINER")

# Database connection parameters
conn_params = {
    'dbname': os.environ.get("POSTGRES_DB_NAME"),
    'user': os.environ.get("POSTGRES_USER"),
    'password': os.environ.get("POSTGRES_PASSWORD"),
    'host': os.environ.get("POSTGRES_HOST"),
    'port': os.environ.get("POSTGRES_PORT"),
    'sslmode': os.environ.get("POSTGRES_SSLMODE")
}

@app.post("/registration")
def registration(user: RegistrationModel):
    """
    Register a new user in the system.
    
    Args:
        user (RegistrationModel): The user registration data containing `email`, `password`, 
                                   `first_name`, and `last_name`.
    
    Returns:
        dict: A dictionary containing status code and message indicating whether the registration was successful or failed.
    
    Raises:
        Exception: Any exception that occurs while connecting to the database or executing the query.
    """
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(**conn_params)
        print("Connected to the database!")
        
        cursor = conn.cursor()
        
        # Create table if it does not exist
        cursor.execute("CREATE TABLE IF NOT EXISTS users (email VARCHAR(255) PRIMARY KEY, password VARCHAR(255), first_name VARCHAR(255), last_name VARCHAR(255));")
        
        # Insert user data into the database
        cursor.execute("INSERT INTO users (email, password, first_name, last_name) VALUES (%s, %s, %s, %s);", 
                       (user.email, user.password, user.first_name, user.last_name))
        
        # Commit the transaction
        conn.commit()

    except Exception as e:
        print("Error connecting to the database:", e)
        return {
            "status_code": 400,
            "message": "Error connecting to the database",
        }
    finally:
        if conn:
            cursor.close()
            conn.close()
        print("Connection closed.")

    return {
        "status_code": 201,
        "message": "User registered successfully",
    }

@app.post("/auth")
def login(login: Login):
    """
    Authenticate a user.
    
    Args:
        login (Login): The login data containing `username` and `password`.
    
    Returns:
        dict: A dictionary containing status code and message indicating the authentication result.
    """
    return {
        "status_code": 200,
        "message": "User authenticated successfully",
    }

@app.post("/upload-legal-doc")
def upload_legal_doc(request: Request, file: UploadFile = File(...)):
    """
    Upload a legal document to Azure Blob Storage.
    
    Args:
        request (Request): The request object.
        file (UploadFile): The legal document file to be uploaded.
    
    Returns:
        dict: A dictionary containing the status code and message indicating whether the file upload was successful or failed.
    
    Raises:
        Exception: Any exception that occurs while uploading the file to Azure Blob Storage.
    """
    blob_database = BlobStorageDatabase()
    blob_client = blob_database.blob_service_client.get_blob_client(container=AZURE_BLOB_CONTAINER, blob=file.filename)

    try:
        # Upload the file to Azure Blob Storage
        blob_client.upload_blob(file.file)
        print(f"File uploaded: {file.filename}")

        # final testing pending to create index via api
        # data_ingestor = DataIngestor()
        # data_ingestor.ingest_data(file.filename)

    except Exception as e:
        return {
            "status_code": 400,
            "message": f"File upload failed: {str(e)}"
        }
    finally:
        file.file.close()

    message = f"{file.filename} - Legal document uploaded successfully"
    
    return {
        "status_code": 200,
        "message": message,
    }

@app.post("/legal-bot")
def legal_bot(request: Request, query_data: ChatQueryModel):
    """
    Query the legal chatbot for responses to user queries.
    
    Args:
        request (Request): The request object.
        query_data (ChatQueryModel): The user's query input in the `query` field.
    
    Returns:
        dict: A dictionary containing status code and the chatbot's response to the query.
    """
    content_generation_object = QueryResponseGenerator()
    
    # Query the chatbot for a response
    response = content_generation_object.get_chat_query_response(query_data.query)

    return {
        "status_code": 200,
        "message": response,
    }

@app.get("/list-users")
def list_users():
    """
    List all registered users.
    
    This endpoint retrieves all users from the `users` table.
    
    Returns:
        dict: A dictionary containing the status code, a message, and a list of all users.
    
    Raises:
        Exception: Any exception that occurs while connecting to the database or retrieving users.
    """
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(**conn_params)
        print("Connected to the database!")
        
        cursor = conn.cursor()
        
        # Retrieve all users from the database
        cursor.execute("SELECT * FROM users;")
        users = cursor.fetchall()
        print("Users:", users)

    except Exception as e:
        print("Error connecting to the database:", e)
        return {
            "status_code": 400,
            "message": "Error connecting to the database",
        }
    finally:
        if conn:
            cursor.close()
            conn.close()
        print("Connection closed.")

    return {
        "status_code": 200,
        "message": "Users listed successfully",
        "users": users
    }
