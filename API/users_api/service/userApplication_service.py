from app.db import db
from schemas.users_schemas import User_application, Progress
#from app.schemas.resourses_schemas import sentences, texts, words, TextsEvaluation, SentencesEvaluation
from google.cloud.firestore_v1 import FieldFilter
from fastapi import HTTPException, UploadFile, Form
from firebase_admin import storage

class UserApplicationService:
    """Service for userapplication-related operations in the Firestore database."""
    
    def __init__(self):
        self.collection = db.collection("user_application")

    async def post_user_application_service(self, user_application: User_application):

        try:
            doc_ref = self.collection.add(user_application.model_dump())
            return {"message": "User add", "doc_id": doc_ref[1].id}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error adding user: {str(e)}")

    async def post_user_application_progress_service(self, uid_userApplication: str, progress: Progress):
        try:
            data = progress.model_dump()
            progress_ref = self.collection.document(uid_userApplication).collection("progress")
            doc_ref = progress_ref.add(data)
            return {"message": "Progress add", "doc_id": doc_ref[1].id}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error adding progress: {str(e)}")
    
    async def get_user_application_progress_uiduser_uidresource_service(self,uid_userApplication: str, uid_resource: str):
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
        try:
            user_ref = self.collection.document(uid_user_application)
            doc = user_ref.get()

            if not doc.exists:
                raise HTTPException(status_code=404, detail="user not found")

            return {"id": doc.id, **doc.to_dict()}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")

