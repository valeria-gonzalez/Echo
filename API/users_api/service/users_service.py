from app.db import db
from utils.hash import Hash
from schemas.users_schemas import User
from google.cloud.firestore_v1 import FieldFilter
from fastapi import HTTPException, UploadFile, Form
from firebase_admin import storage

class UsersService:
    """
    Service class for user-related operations in the Firestore database.

    This class provides methods for creating, retrieving, and managing users
    in Firestore. It also includes utilities for handling password hashing
    and file uploads (e.g., profile images) using Firebase Storage.

    Attributes:
        collection: Reference to the Firestore users collection.
    """
    def __init__(self):
        self.collection = db.collection("users")

    async def get_users_by_uid_service(self,uid_user:str) -> dict:
        """
        Retrieves a user from Firestore by their UID.

        Args:
            uid_user (str): User's unique identifier (UID).

        Returns:
            dict: User information including document ID.

        Raises:
            HTTPException: If the user is not found or an internal error occurs.
        """

        try:
            user_ref = self.collection.document(uid_user)
            doc = user_ref.get()

            if not doc.exists:
                raise HTTPException(status_code=404, detail="user not found")

            return {"id": doc.id, 
                    **doc.to_dict()
                    }
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error {str(e)}"
                )

    async def post_users_service(self, user: User) -> dict:
        """
        Adds a new user to Firestore after hashing their password.

        Args:
            user (User): User object containing user data.

        Returns:
            dict: A message confirming the addition and the Firestore document ID.

        Raises:
            HTTPException: If an error occurs while adding the user.
        """

        query = self.collection.where("email", "==", user.email).limit(1)
        docs = query.stream()
        doc = next(docs, None)

        if doc is not None and doc.exists:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )

        try:
            hash_password = Hash.hash_password(user.password)
            user.password = hash_password
            doc_ref = self.collection.add(user.model_dump())
            return {"message": "User add", 
                    "doc_id": doc_ref[1].id}
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail="Error adding user"
                )

    async def get_users_by_email_service(self,email:str):
        """
        Retrieves a user from Firestore by their email.

        Args:
            email (str): User's email address.

        Returns:
            dict: User information.

        Raises:
            HTTPException: If the user is not found or an internal error occurs.
        """
        try:
            query = self.collection.where("email", "==", email).limit(1)
            docs = query.stream()
            doc = next(docs, None)
            if doc is None or not doc.exists:
                raise HTTPException(status_code=404, detail="user not found")

            return {"id": doc.id, **doc.to_dict()}
        
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error {str(e)}"
                )
