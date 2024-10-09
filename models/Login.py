from pydantic import BaseModel, validator

class Login(BaseModel):
    """
    This model is used to validate user credentials (username and password) when performing a login action.
    It ensures that both `username` and `password` are provided and are non-empty strings.
    
    Attributes:
        username (str): The username provided by the user for login. It must be a non-empty string.
        password (str): The password provided by the user for login. It must be a non-empty string.
    
    Validation:
        - `username`: Must not be empty. A `ValueError` will be raised if it is missing.
        - `password`: Must not be empty. A `ValueError` will be raised if it is missing.
    
    Raises:
        ValueError: If `username` or `password` is empty or not provided.
    """

    username: str
    password: str

    @validator('username')
    def validate_username(cls, v):
        """
        Validator for `username` field.

        This method checks that the `username` field is not empty. 
        If the value is empty or None, a `ValueError` is raised.

        Args:
            v (str): The value of the `username` field to be validated.

        Returns:
            str: The validated (non-empty) username.

        Raises:
            ValueError: If `username` is empty or None.
        """
        if not v:
            raise ValueError('Username is required')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        """
        Validator for `password` field.

        This method checks that the `password` field is not empty.
        If the value is empty or None, a `ValueError` is raised.

        Args:
            v (str): The value of the `password` field to be validated.

        Returns:
            str: The validated (non-empty) password.

        Raises:
            ValueError: If `password` is empty or None.
        """
        if not v:
            raise ValueError('Password is required')
        return v
