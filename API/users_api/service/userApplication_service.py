from app.db import db
from schemas.users_schemas import User_application, Progress
from google.cloud.firestore_v1 import FieldFilter
from fastapi import HTTPException

class UserApplicationService:
    def __init__(self):
        self.collection = db.collection("user_application")

    async def post_user_application_service(self, user_application: User_application):   
        try:
            doc_ref = self.collection.add(user_application.model_dump())
            return {"message": "User add", "doc_id": doc_ref[1].id}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error adding user: {str(e)}")

    async def post_user_application_progress_service(self, uid_user: str, progress: Progress):
        try:
            query = self.collection.where("user_uid", "==", uid_user).limit(1)
            docs = query.stream()
            doc = next(docs,None)
            if not doc:
                raise HTTPException(status_code=404, detail="user not found")
            
            progress_ref = self.collection.document(doc.id).collection("progress")

            data = progress.model_dump()

            existing_query = progress_ref.where("resource_uid","==",data["resource_uid"]).limit(1).stream()
            existing_doc = next(existing_query, None)

            if(existing_doc):
                progress_ref.document(existing_doc.id).update(data)
                return {"message": "progress update", "doc_id":existing_doc.id}
            else:
                new_doc = progress_ref.add(data)[1]
                return {"message": "progress added", "doc_id":new_doc.id}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error adding progress: {str(e)}")
    
    async def get_user_progress_by_resource_uid(self,uid_userApplication: str, uid_resource: str):
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
        
    async def get_users_application_by_user_uid_service(self,
                                                        uid_user:str):
        try:
            query = self.collection.where("user_uid", "==", uid_user).limit(1)
            docs = query.stream()
            doc = next(docs,None)

            if not doc:
                raise HTTPException(status_code=404, detail="user not found")

            result = {
                "id": doc.id,
                **doc.to_dict()
            }
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")

        
    async def get_user_progress_by_attempts_uid(self,
                                                uid_user: str):

        try:
            query = self.collection.where("user_uid", "==", uid_user).limit(1)
            docs = query.stream()
            doc = next(docs,None)
            if not doc:
                raise HTTPException(status_code=404, detail="user not found")
            
            progress_ref = self.collection.document(doc.id).collection("progress")
            result = progress_ref.stream()

            progress_by_uid = []
            for doc in result:
                data= doc.to_dict()

                if "attempts" in data and isinstance(data["attempts"], (int,float)) and data["attempts"] > 0:
                    progress_by_uid.append({"id": doc.id,
                                            **data})

            if not progress_by_uid:
                raise HTTPException(status_code=404,detail="progress not found")

            return progress_by_uid
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")


    async def get_user_progress_by_completed_user_uid(self,
                                                    uid_user: str):

        try:
            query = self.collection.where("user_uid", "==", uid_user).limit(1)
            docs = query.stream()
            doc = next(docs,None)
            if not doc:
                raise HTTPException(status_code=404, detail="user not found")
            
            progress_ref = self.collection.document(doc.id).collection("progress")
            result = progress_ref.stream()

            progress_by_uid = []
            for doc in result:
                data= doc.to_dict()

                if "completed" in data and isinstance(data["completed"], (bool)) and data["completed"] == True:
                    progress_by_uid.append({"id": doc.id,
                                            **data})

            if not progress_by_uid:
                raise HTTPException(status_code=404,detail="progress not found")

            return progress_by_uid
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")

        