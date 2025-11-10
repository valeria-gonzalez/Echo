# utils/jwt_handler.py
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 720

def create_access_token(data: dict):
    """
    Creates a new JWT access token with an expiration time.

    This function generates a signed JSON Web Token (JWT) that includes 
    the provided payload data and an expiration timestamp. The token is 
    encoded using the application's secret key and the defined algorithm.

    Args:
        data (dict): A dictionary containing user-related claims 
            (e.g., {'sub': user_id}) to be embedded in the token.

    Returns:
        str: The encoded JWT as a string.

    Raises:
        Exception: If an unexpected error occurs during token generation.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """
    Verifies and decodes a JWT access token.

    This function decodes the provided JWT using the application's secret key
    and validates its structure. It ensures that the token contains a valid
    'sub' (subject) claim representing the authenticated user's ID.

    Args:
        token (str): The JWT access token to be verified.

    Returns:
        str: The user ID extracted from the token's payload.

    Raises:
        HTTPException:
            - 401 Unauthorized: If the token is invalid, expired, or missing the 'sub' field.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
