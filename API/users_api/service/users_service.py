from app.db import db
from schemas.users_schemas import User
from google.cloud.firestore_v1 import FieldFilter
from fastapi import HTTPException, UploadFile, Form
from firebase_admin import storage

class UsersService:
    """Service for user-related operations in the Firestore database."""
    
    def __init__(self):
        self.collection = db.collection("users")

    async def get_users_by_uid_service(self,uid_user:str):
        """
        Get the information about the collection users with specific uid

        Args:

            uuid_user(str): user from whom we want the information

        Returns:
            return collection with the uid

        Raises:
            HttpEXception: If an error occurs
        """
        try:
            user_ref = self.collection.document(uid_user)
            doc = user_ref.get()

            if not doc.exists:
                raise HTTPException(status_code=404, detail="user not found")

            return {"id": doc.id, **doc.to_dict()}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")

    async def post_users_service(self, user: User):

        """
        Add the data to the collection users

        Args:
            user(User): user data we want add to the collection

        Returns:
            Message "user add" if all is ok

        Raises:
            HttpEXception: If an error occurs
        """
        try:
            doc_ref = self.collection.add(user.model_dump())
            return {"message": "User add", "doc_id": doc_ref[1].id}
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error adding user")

    