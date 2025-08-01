from app.db import db
from schemas.users_schemas import User_application, Progress
from google.cloud.firestore_v1 import FieldFilter
from fastapi import HTTPException

class UserApplicationService:
    """Service for userapplication-related operations in the Firestore database."""
    
    def __init__(self):
        self.collection = db.collection("user_application")

    async def post_user_application_service(self, user_application: User_application):
        """
        Adds a new user application document to the firebase

        Args:
            user_application(User_application): The user application data to be saved
        
        Returns:
            dict: A message confirming the addition

        Raises:
            HttpEXception: If an error occurs
        """
        
        try:
            doc_ref = self.collection.add(user_application.model_dump())
            return {"message": "User add", "doc_id": doc_ref[1].id}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error adding user: {str(e)}")

    async def post_user_application_progress_service(self, uid_userApplication: str, progress: Progress):
        """
        Adds a progress using uid_userApplication

        Args:

            uid_userApplication(str): user uid to which we want to add the progress
            progress(Progress): It is the information that contains the progress 
        
        Returns:
            dict: A message confirming the addition

        Raises:
            HttpEXception: If an error occurs
        """
        
        try:
            data = progress.model_dump()
            progress_ref = self.collection.document(uid_userApplication).collection("progress")
            doc_ref = progress_ref.add(data)
            return {"message": "Progress add", "doc_id": doc_ref[1].id}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error adding progress: {str(e)}")
    
    async def get_user_progress_by_resource_uid(self,uid_userApplication: str, uid_resource: str):
        """
        Get all the progress of a user with the resource uid

        Args:

            uid_userApplication(str): user from whom we want the information
            uid_resource(Progress): uid of the resource we want to know its progress
        
        Returns:
            progress_by_uid (List(dic)) list with json with the progress related to the user and that resource

        Raises:
            HttpEXception: If an error occurs
        """
        try:
            progress_ref = self.collection.document(uid_userApplication).collection("progress")
            query = progress_ref.where(filter=FieldFilter("resource_uid","==", uid_resource))
            result = query.stream()

            progress_by_uid = []
            for doc in result:
                progress_by_uid.append({"id": doc.id, **doc.to_dict()})
            if not progress_by_uid:
                raise HTTPException(status_code=404,detail="progress not found")

            return progress_by_uid
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def get_users_application_by_uid_service(self,uid_user_application:str):
        """
        Get the information about the collection user_application with specific uid

        Args:

            uid_user_application(str): user from whom we want the information

        Returns:
            return collection with the uid

        Raises:
            HttpEXception: If an error occurs
        """
        try:
            user_ref = self.collection.document(uid_user_application)
            doc = user_ref.get()

            if not doc.exists:
                raise HTTPException(status_code=404, detail="user not found")

            return {"id": doc.id, **doc.to_dict()}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")

