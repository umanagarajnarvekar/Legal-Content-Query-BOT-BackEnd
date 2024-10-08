from pydantic import BaseModel, EmailStr, validator

class RegistrationModel(BaseModel):
    '''
    Registration model for user registration
    '''
    email: EmailStr
    password: str
    first_name: str
    last_name: str

    @validator('email')
    def validate_email(cls, v):
        '''
        Validate email
        '''
        if not v:
            raise ValueError('Email is required')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        '''
        Validate password
        '''
        if len(v) < 6:
            raise ValueError('Password must be at least 8 characters long')
        return v
    
    @validator('first_name')
    def validate_first_name(cls, v):
        '''
        Validate first name
        '''
        if not v:
            raise ValueError('First name is required')
        return v
    
    @validator('last_name')
    def validate_last_name(cls, v):
        '''
        Validate last name
        '''
        if not v:
            raise ValueError('Last name is required')
        return v


