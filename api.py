import os
from fastapi import FastAPI, File, UploadFile, Request
import psycopg2
from dotenv import load_dotenv
from models.RegistrationModel import RegistrationModel
from models.Login import Login
from models.ChatQueryModel import ChatQueryModel
from db.blob_storage import BlobStorageDatabase
from rag.QueryResponseGenerator import QueryResponseGenerator
from rag.PdfDataIngestor import DataIngestor

app = FastAPI()
load_dotenv()

AZURE_BLOB_CONTAINER = os.environ.get("AZURE_BLOB_CONTAINER")

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
    Register a new user
    """
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(**conn_params)
        print("Connected to the database!")
        
        # Create a cursor object
        cursor = conn.cursor()
        
        #create table if not exists
        cursor.execute("CREATE TABLE IF NOT EXISTS users (email VARCHAR(255) PRIMARY KEY, password VARCHAR(255), first_name VARCHAR(255), last_name VARCHAR(255));")

        # Insert a row
        cursor.execute("INSERT INTO users (email, password, first_name, last_name) VALUES (%s, %s, %s, %s);", (user.email, user.password, user.first_name, user.last_name))

        # Commit changes
        conn.commit()


        # # Execute a query
        # cursor.execute("SELECT version();")
        # version = cursor.fetchone()
        # print("PostgreSQL version:", version)

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
    Authenticate a user
    """
    return {
        "status_code": 200,
        "message": "User authenticated successfully",
    }

@app.post("/upload-legal-doc")
def upload_legal_doc(request: Request, file: UploadFile = File(...)):
    """
    Upload legal document
    """
    blob_database = BlobStorageDatabase()
    blob_client = blob_database.blob_service_client.get_blob_client(container=AZURE_BLOB_CONTAINER, blob=file.filename)

    try:
        # Upload the file to Azure Blob Storage
        blob_client.upload_blob(file.file)
        print(f"File uploaded: {file.filename}")
        # data_ingestor = DataIngestor()
        # result = data_ingestor.ingest_data(file.filename)

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
    Legal bot
    """

    content_generation_object = QueryResponseGenerator()
    # query to retrieve documents
    response = content_generation_object.get_chat_query_response(query_data.query)

    return {
        "status_code": 200,
        "message": response,
    }

@app.get("/list-users")
def list_users():
    """
    List users
    """
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(**conn_params)
        print("Connected to the database!")
        
        # Create a cursor object
        cursor = conn.cursor()
        
        # Execute a query
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
