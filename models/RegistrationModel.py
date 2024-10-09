from pydantic import BaseModel, EmailStr, validator

class RegistrationModel(BaseModel):
    """
    This model is used to validate the required information when registering a new user. It ensures that:
    - The `email` is a valid email format.
    - The `password` is at least 6 characters long.
    - Both `first_name` and `last_name` are provided and are non-empty strings.

    Attributes:
        email (EmailStr): The user's email address. Must be a valid email format.
        password (str): The user's password. Must be at least 6 characters long.
        first_name (str): The user's first name. Must be a non-empty string.
        last_name (str): The user's last name. Must be a non-empty string.
    
    Raises:
        ValueError: If any field does not conform to the validation criteria.
    """

    email: EmailStr
    password: str
    first_name: str
    last_name: str

    @validator('email')
    def validate_email(cls, v):
        """
        Ensures that the email is not empty. Since `EmailStr` type is used, Pydantic already checks for
        valid email format, but this validator ensures that the email field is provided.

        Args:
            v (str): The value of the `email` field to be validated.

        Returns:
            str: The validated email address.

        Raises:
            ValueError: If the email is empty or None.
        """
        if not v:
            raise ValueError('Email is required')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        """
        Ensures that the password is at least 6 characters long.

        Args:
            v (str): The value of the `password` field to be validated.

        Returns:
            str: The validated password.

        Raises:
            ValueError: If the password is less than 6 characters long.
        """
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v
    
    @validator('first_name')
    def validate_first_name(cls, v):
        """
        Ensures that the first name is provided and is not empty.

        Args:
            v (str): The value of the `first_name` field to be validated.

        Returns:
            str: The validated first name.

        Raises:
            ValueError: If the first name is empty or None.
        """
        if not v:
            raise ValueError('First name is required')
        return v
    
    @validator('last_name')
    def validate_last_name(cls, v):
        """
        Ensures that the last name is provided and is not empty.

        Args:
            v (str): The value of the `last_name` field to be validated.

        Returns:
            str: The validated last name.

        Raises:
            ValueError: If the last name is empty or None.
        """
        if not v:
            raise ValueError('Last name is required')
        return v
