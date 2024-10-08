from fastapi import FastAPI

from models import RegistrationModel
app = FastAPI()

@app.post("/registration")
def registration(user: RegistrationModel):
    """
    Register a new user
    """
    return {
        "status_code": 201,
        "message": "User registered successfully",
    }

    