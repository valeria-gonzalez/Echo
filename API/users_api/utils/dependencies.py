from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from utils.jwt_handler import verify_token

security = HTTPBearer()

def get_current_user(credentials=Depends(security)):
    """
    Extracts and verifies the JWT token from the request's Authorization header.

    This dependency retrieves the Bearer token provided by the client, 
    verifies its authenticity using the application's secret key, and 
    extracts the authenticated user's ID. It is intended to be used in 
    protected routes to ensure that only authenticated users can access them.

    Args:
        credentials (HTTPAuthorizationCredentials): Automatically provided by 
            FastAPI's HTTPBearer dependency, containing the Bearer token.

    Returns:
        str: The user ID extracted from the verified JWT.

    Raises:
        HTTPException:
            - 401 Unauthorized: If the token is missing, invalid, or expired.
    """
    token = credentials.credentials
    user_id = verify_token(token)
    return user_id