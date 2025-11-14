from fastapi import APIRouter,HTTPException, UploadFile, File
from service.users_service import UsersService
from service.userApplication_service import UserApplicationService
from schemas.users_schemas import User, User_application, Progress
from fastapi import Depends
from utils.dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Information about users"],
)

users_application_service = UserApplicationService()
users_service = UsersService()

@router.get("/")
async def root():
    """
    Root endpoint for the Users API.

    Returns:
        dict: A welcome message indicating the API is running.
    """
    return {"message": "Welcome to the Users API!"}

@router.get("/account/{uid_user}")
async def get_users_by_uid_router(
    uid_user:str,
    current_user: dict = Depends(get_current_user)
    ):
    """
    Retrieves a user by their UID.

    Args:
        uid_user (str): The unique identifier of the user.

    Returns:
        dict: The user's data including the Firestore document ID.

    Raises:
        HTTPException:
            - 404 Not Found: If the user is not found.
            - 500 Internal Server Error: If an unexpected error occurs while fetching the user.
    """
    usersService = UsersService()
    try:

        return await usersService.get_users_by_uid_service(
            uid_user=uid_user
            )
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error: {str(e)}"
            )
    
@router.get("/user_application/{uid_user}")
async def get_users_by_uid_router(
    uid_user:str,
    current_user: dict = Depends(get_current_user) 
    ):
    """
    Retrieves a user application by the user's UID.

    Args:
        uid_user (str): The unique identifier of the user.

    Returns:
        dict: The user's application data including the Firestore document ID.

    Raises:
        HTTPException:
            - 404 Not Found: If the user application is not found.
            - 500 Internal Server Error: If an unexpected error occurs while fetching the data.
    """

    try:
        return await users_application_service.get_users_application_by_user_uid_service(
            uid_user=uid_user
            )
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error: {str(e)}"
            )

@router.post("/account")
async def post_users_router(
    user:User
    ):
    """
    Adds a new user to Firestore.

    Args:
        user (User): The user object containing user data.

    Returns:
        dict: A confirmation message with the Firestore document ID.

    Raises:
        HTTPException:
            - 500 Internal Server Error: If an unexpected error occurs while adding the user.
    """
    try:
        return await users_service.post_users_service(
            user=user
            )
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error adding user: {str(e)}"
            )
        
@router.post("/user_application")
async def post_users_application_router(
    user_application:User_application
    ):
    """
    Adds a new user application record to Firestore.

    Args:
        user_application (User_application): The user application object containing user data.

    Returns:
        dict: A confirmation message with the Firestore document ID.

    Raises:
        HTTPException:
            - 500 Internal Server Error: If an unexpected error occurs while adding the user application.
    """

    try:
        return await users_application_service.post_user_application_service(
            user_application=user_application
            )
    
    except HTTPException:
        raise 
    
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error adding user application: {str(e)}"
            )
    
@router.put("/user_application")
async def post_users_application_router(
    user_application:User_application,
    current_user: dict = Depends(get_current_user) 
    ):
    """
    Updates an existing user application record in Firestore.

    Args:
        user_application (User_application): The user application object containing updated data.

    Returns:
        dict: A confirmation message with the Firestore document ID.

    Raises:
        HTTPException:
            - 404 Not Found: If the user is not found.
            - 500 Internal Server Error: If an unexpected error occurs while updating the application.
    """

    try:
        return await users_application_service.update_user_application_service(
            user_application=user_application
            )
    
    except HTTPException:
        raise 
    
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error updating user application: {str(e)}"
            )
    
@router.post("/user_application/progress/{uid_user}")
async def post_users_application_progress_router(
    uid_user:str, 
    progress:Progress,
    current_user: dict = Depends(get_current_user) 
    ):
    """
    Adds or updates a user's progress record for a specific resource within their application.

    If a progress record for the same resource already exists, it updates it; otherwise, it creates a new record.

    Args:
        uid_user (str): The unique identifier of the user.
        progress (Progress): The progress object containing resource progress data.

    Returns:
        dict: A confirmation message with the Firestore document ID.

    Raises:
        HTTPException:
            - 404 Not Found: If the user is not found.
            - 500 Internal Server Error: If an unexpected error occurs while adding/updating progress.
    """

    try:
        return await users_application_service.post_user_application_progress_service(
            uid_user=uid_user, 
            progress=progress
            )
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error: {str(e)}"
            )
    
@router.get("/progress/attempts/{uid_user}")
async def get_users_application_progress_attempts_uid_router(
    uid_user: str,
    current_user: dict = Depends(get_current_user) 
    ):
    """
    Retrieves all progress records with attempts greater than zero for a specific user.

    Args:
        uid_user (str): The unique identifier of the user.

    Returns:
        list[dict]: A list of progress records with attempts > 0, each including the document ID and data.

    Raises:
        HTTPException:
            - 404 Not Found: If no progress with attempts > 0 is found for the user.
            - 500 Internal Server Error: If an unexpected error occurs during retrieval.
    """
    try:
        return await users_application_service.get_user_progress_by_attempts_uid(
            uid_user=uid_user
            )
    except HTTPException:
        raise 
    
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error: {str(e)}"
            )
    
    
@router.get("/progress/completed/{uid_user}")
async def get_users_application_progress_completed_uid_router(
    uid_user: str,
    current_user: dict = Depends(get_current_user)
    ):
    """
    Retrieves all completed progress records for a specific user's application.

    Args:
        uid_user (str): The unique identifier of the user's application.

    Returns:
        list[dict]: A list of completed progress records, each including the document ID and data.

    Raises:
        HTTPException:
            - 404 Not Found: If no completed progress is found for the user.
            - 500 Internal Server Error: If an unexpected error occurs during retrieval.
    """
    result = await users_application_service.get_user_progress_by_completed_user_uid(uid_user)

    if result is None:
        return {"detail": "Progress not found"}  # still status 200

    return result
    
@router.get("/progress/{uid_user_application}/{uid_resource}")
async def get_users_application_progress_uid_router(
    uid_user_application: str, 
    uid_resource:str,
    current_user: dict = Depends(get_current_user)
    ):
    """
    Retrieves progress records for a specific resource within a user's application.

    Args:
        uid_user_application (str): The unique identifier of the user's application.
        uid_resource (str): The unique identifier of the resource.

    Returns:
        list[dict]: A list of progress records for the specified resource, each including the document ID and data.

    Raises:
        HTTPException:
            - 404 Not Found: If no progress is found for the resource.
            - 500 Internal Server Error: If an unexpected error occurs during retrieval.
    """
    try:
        return await users_application_service.get_user_progress_by_resource_uid(
            uid_userApplication=uid_user_application, 
            uid_resource=uid_resource
            )
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error: {str(e)}"
            )

@router.post("/user_application/profile_picture/{user_uid}")
async def post_image_router(
    user_uid: str, 
    file: UploadFile = File(...)
    ):
    """
    Uploads a profile picture for a user and updates its URL in Firestore.

    Args:
        user_uid (str): The unique identifier of the user.
        file (UploadFile): The image file to upload.

    Returns:
        dict: Confirmation message if the upload and URL update succeed.

    Raises:
        HTTPException: 
            - 500 Internal Server Error: If an error occurs during upload or URL update.
    """

    try:
        return await users_application_service.post_image(
            file=file, 
            user_uid=user_uid
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error: {str(e)}"
            )