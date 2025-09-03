from fastapi import APIRouter,HTTPException, UploadFile, File
from service.users_service import UsersService
from schemas.users_schemas import BodyLogin
from utils.hash import Hash

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)
"""
Authentication router for handling user login.

This module provides endpoints for authenticating users using their email
and password. Passwords are verified using hashed comparison.
"""


users_service = UsersService()

@router.post("/login")
async def login_router(data:BodyLogin):
    """
    Authenticates a user by their email and password.

    Args:
        data (BodyLogin): The login data containing 'email' and 'password'.

    Returns:
        dict: A confirmation message and the user ID if authentication succeeds.

    Raises:
        HTTPException: 
            - 401 Unauthorized: If the email or password is incorrect.
            - 500 Internal Server Error: If an unexpected error occurs during login.
    """
    try:

        user = await users_service.get_users_by_email_service(data.email)
        print(user)
        if not user:
            raise HTTPException(
                status_code = 401, 
                detail = "user not found"
                )

        if not Hash.verify_password(data.password, user["password"]):
            raise HTTPException(
                status_code = 401, 
                detail= "incorrect password"
                )

        
        return{"message": "login successful"}

    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code = 500,  
            detail = f"login error {e}"
            )