from pydantic import BaseModel, validator


class Login(BaseModel):
    '''
    Login model for user login
    '''
    username: str
    password: str

    @validator('username')
    def validate_username(cls, v):
        '''
        Validate username
        '''
        if not v:
            raise ValueError('Username is required')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        '''
        Validate password
        '''
        if not v:
            raise ValueError('Password is required')
        return v
    