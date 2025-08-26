from fastapi import APIRouter,HTTPException
from service.users_service import UsersService
from service.userApplication_service import UserApplicationService
from schemas.users_schemas import User, User_application, Progress

router = APIRouter(
    prefix="/users",
    tags=["Information about users"],
)

usersApplicationService = UserApplicationService()
usersService = UsersService()

@router.get("/")
async def root():
    return {"message": "Welcome to the Users API!"}

@router.get("/account/{uid_user}")
async def get_users_by_uid_router(uid_user:str):
    try:
        usersService = UsersService()
        return await usersService.get_users_by_uid_service(uid_user=uid_user)
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
@router.get("/user_application/{uid_user}")
async def get_users_by_uid_router(uid_user:str):
    try:
        return await usersApplicationService.get_users_application_by_user_uid_service(uid_user=uid_user)
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.post("/account")
async def post_users_router(user:User):
    try:
        return await usersService.post_users_service(user=user)
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error")
        
@router.post("/user_application")
async def post_users_application_router(user_application:User_application):
    try:
        return await usersApplicationService.post_user_application_service(user_application=user_application)
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
@router.post("/user_application/progress/{uid_user}")
async def post_users_application_progress_router(uid_user:str, progress:Progress):
    try:
        return await usersApplicationService.post_user_application_progress_service(uid_user=uid_user, progress=progress)
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
@router.get("/progress/attempts/{uid_user}")
async def get_users_application_progress_attempts_uid_router(uid_user: str):
    try:
        return await usersApplicationService.get_user_progress_by_attempts_uid(uid_user=uid_user)
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
    
@router.get("/progress/completed/{uid_user_application}")
async def get_users_application_progress_completed_uid_router(uid_user_application: str):
    try:
        return await usersApplicationService.get_user_progress_by_completed_user_uid(uid_user=uid_user_application)
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
@router.get("/progress/{uid_user_application}/{uid_resource}")
async def get_users_application_progress_uid_router(uid_user_application: str, uid_resource:str):
    try:
        return await usersApplicationService.get_user_progress_by_resource_uid(uid_userApplication=uid_user_application, uid_resource=uid_resource)
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

