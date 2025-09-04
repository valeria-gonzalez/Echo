from app.db import db
from schemas.users_schemas import User_application, Progress
from google.cloud.firestore_v1 import FieldFilter
from fastapi import HTTPException, UploadFile
from firebase_admin import storage

class UserApplicationService:
    """
    Service class for handling operations related to user applications in Firestore.

    This class provides methods for creating, retrieving, and updating user application
    records in the Firestore 'user_application' collection.

    Attributes:
        collection: Reference to the Firestore 'user_application' collection.
    """

    def __init__(self):
        self.collection = db.collection("user_application")

    async def post_user_application_service(
            self, 
            user_application: User_application
            ):   
        """
        Adds a new user application record to Firestore.

        Args:
            user_application (User_application): The user application object containing user data.

        Returns:
            dict: A confirmation message with the Firestore document ID.

        Raises:
            HTTPException: If an error occurs while adding the user application.
        """

        try:
            doc_ref = self.collection.add(user_application.model_dump())
            return {
                "message": "User add",
                "doc_id": doc_ref[1].id
                }
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error adding user: {str(e)}"
                )

    async def update_user_application_service(
            self, 
            user_application: User_application
            ) -> dict:   
        """
        Updates an existing user application record in Firestore.

        Args:
            user_application (User_application): The user application object containing updated data.

        Returns:
            dict: A confirmation message with the Firestore document ID.

        Raises:
            HTTPException: If the user is not found or an error occurs while updating the application.
        """

        try:
            query = self.collection.where("user_uid", "==", user_application.user_uid).limit(1)
            docs = query.stream()
            doc = next(docs,None)
            if not doc:
                raise HTTPException(status_code=404, detail="user not found")
            
            doc_ref = self.collection.document(doc.id)
            data = user_application.model_dump()
            doc_ref.update(data)

            return {
                "message": "user_application update",
                "doc_id":doc_ref.id
                }
        
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error update users_application : {str(e)}"
                )

    async def post_user_application_progress_service(
            self, 
            uid_user: str, 
            progress: Progress
            ) ->dict:
        """
        Adds or updates a user's progress record for a specific resource within their application.

        If a progress record for the same resource already exists, it updates it;
        otherwise, it creates a new progress record.

        Args:
            uid_user (str): The unique identifier of the user.
            progress (Progress): The progress object containing resource progress data.

        Returns:
            dict: A confirmation message with the Firestore document ID.

        Raises:
            HTTPException: If the user is not found or an error occurs while adding/updating progress.
        """

        try:
            query = self.collection.where("user_uid", "==", uid_user).limit(1)
            docs = query.stream()
            doc = next(docs,None)
            if not doc:
                raise HTTPException(
                    status_code=404, 
                    detail="user not found"
                    )
            
            progress_ref = self.collection.document(doc.id).collection("progress")

            data = progress.model_dump()

            existing_query = progress_ref.where("resource_uid","==",data["resource_uid"]).limit(1).stream()
            existing_doc = next(existing_query, None)

            if(existing_doc):
                progress_ref.document(existing_doc.id).update(data)
                return {
                    "message": "progress update", 
                    "doc_id":existing_doc.id
                }
            else:
                new_doc = progress_ref.add(data)[1]
                return {
                    "message": "progress added",
                    "doc_id":new_doc.id
                }
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error adding progress: {str(e)}"
                )
    
    async def get_user_progress_by_resource_uid(
            self,
            uid_userApplication: str, 
            uid_resource: str
            ) -> list[dict]:
        """
        Retrieves progress records for a specific resource within a user's application.

        Args:
            uid_userApplication (str): The unique identifier of the user's application.
            uid_resource (str): The unique identifier of the resource.

        Returns:
            list[dict]: A list of progress records for the specified resource, each including the document ID and data.

        Raises:
            HTTPException: If no progress is found for the resource or an internal error occurs.
        """

        try:
            progress_ref = self.collection.document(uid_userApplication).collection("progress")
            query = progress_ref.where(filter=FieldFilter("resource_uid","==", uid_resource))
            result = query.stream()

            progress_by_uid = []
            for doc in result:
                progress_by_uid.append({
                    "id": doc.id, 
                    **doc.to_dict()
                    })
                
            if not progress_by_uid:
                raise HTTPException(
                    status_code=404,
                    detail="progress not found"
                    )

            return progress_by_uid
        
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error {str(e)}"
                )
        
    async def get_users_application_by_user_uid_service(
            self,
            uid_user:str
            ) -> dict:
        """
        Retrieves the application data for a user by their UID.

        Args:
            uid_user (str): The unique identifier of the user.

        Returns:
            dict: The user's application data including the document ID.

        Raises:
            HTTPException: If the user is not found or an internal error occurs.
        """

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
            raise HTTPException(
                status_code=500, 
                detail=f"Error {str(e)}"
                )

        
    async def get_user_progress_by_attempts_uid(
            self,
            uid_user: str
            ) -> list[dict]:
        """
        Retrieves progress records with attempts greater than zero for a user by their UID.

        Args:
            uid_user (str): The unique identifier of the user.

        Returns:
            list[dict]: A list of progress records with attempts > 0, each including the document ID and data.

        Raises:
            HTTPException: If the user is not found, no progress with attempts > 0 is found,
                        or an internal error occurs.
        """

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
                    progress_by_uid.append({
                        "id": doc.id,
                        **data}
                        )

            if not progress_by_uid:
                raise HTTPException(
                    status_code=404,
                    detail="progress not found"
                    )

            return progress_by_uid
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error {str(e)}"
                )


    async def get_user_progress_by_completed_user_uid(
            self,
            uid_user: str
            ) -> list[dict]:
        """
        Retrieves completed progress records for a user by their UID.

        Args:
            uid_user (str): The unique identifier of the user.

        Returns:
            list[dict]: A list of completed progress records, each including the document ID and data.

        Raises:
            HTTPException: If the user is not found, no completed progress is found, or an internal error occurs.
        """

        try:
            query = self.collection.where("user_uid", "==", uid_user).limit(1)
            docs = query.stream()
            doc = next(docs, None)
            if not doc:
                raise HTTPException(status_code=404, detail="user not found")
            
            progress_ref = self.collection.document(doc.id).collection("progress")
            result = progress_ref.stream()

            progress_by_uid = []
            for progress_doc in result:
                data = progress_doc.to_dict()

                if "completed" in data and isinstance(data["completed"], (bool)) and data["completed"] == True:
                    progress_by_uid.append({
                        "id": progress_doc.id,
                        **data
                        })

            if not progress_by_uid:
                raise HTTPException(
                    status_code=404,
                    detail="progress not found"
                    )

            return progress_by_uid
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error {str(e)}"
                )

    async def update_image_url(
            self,
            user_uid: str, 
            url:str
            ):
        """
        Updates the profile image URL for a user in Firestore.

        Args:
            user_uid (str): The unique identifier of the user.
            url (str): The new profile image URL.

        Returns:
            dict: A confirmation message if the update succeeds.

        Raises:
            HTTPException: If no document is found for the user or an internal error occurs.
        """
        try:
    
            query = self.collection.where("user_uid", "==", user_uid) 
            results = list(query.stream())
            
            if not results:
                raise HTTPException(status_code= 404, detail="document not found")
            
            for doc in results:
                doc.reference.update({"profile_picture": url})
            
            return {
                "message": "document update"
                }
        
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error {str(e)}"
                )
        
    async def post_image(
            self,
            file: UploadFile, 
            user_uid: str
            ):
        """
        Uploads a user's profile image to Firebase Storage and updates its URL in Firestore.

        Args:
            file (UploadFile): The image file to be uploaded.
            user_uid (str): The user's unique identifier.

        Returns:
            dict: A confirmation message if the upload and URL update succeed.

        Raises:
            HTTPException: If the file type is invalid or an error occurs during upload.
        """

        if file.content_type not in ["image/png", "image/jpeg", "image/jpg", "image/webp"]:
            raise HTTPException(
                status_code = 400, 
                detail = "unsupported file"
                )
        
        try:
            content = await file.read()
            destination_path_cloud = f"profile_picture/{file.filename}"
            blob = storage.bucket().blob(destination_path_cloud)
            blob.upload_from_string(content, content_type=file.content_type)
            blob.make_public()

            url_public = blob.public_url

            await self.update_image_url(user_uid=user_uid, url=url_public)

            return {
                "message": "Image and url update",
                "image_url": url_public
            }
        
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error {str(e)}"
                )