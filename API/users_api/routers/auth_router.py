from fastapi import APIRouter,HTTPException, UploadFile, File
from service.users_service import UsersService
from schemas.users_schemas import BodyLogin
from utils.hash import Hash
from utils.jwt_handler import create_access_token

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
    try:

        user = await users_service.get_users_by_email_service(data.email)

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

        access_token = create_access_token({"sub": user["id"]})

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user["id"]
        }


    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code = 500,  
            detail = f"login error {e}"
            )