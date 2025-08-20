from app.db import db
from schemas.resources_schemas import texts, TextsEvaluation, TextsAudioDuration
from google.cloud.firestore_v1 import FieldFilter
from fastapi import HTTPException, UploadFile
from firebase_admin import storage

class TextsService():
    def __init__(self):
        self.collection = db.collection("texts")

    async def get_all(self):
        """
        Retrieve all documents from the collection.

        This method streams all documents in the Firestore collection, converts each 
        document to a dictionary, and appends the document ID to the resulting data. 
        It then returns a list containing all documents with their corresponding IDs.

        Returns:
            list[dict]: A list of dictionaries, where each dictionary represents 
            a document from the collection and includes the document ID.
            
        Raises:
            HTTPException: If an error occurs during data retrieval.
        """

        try:
            ref = self.collection.stream()
            all_data = []

            for doc in ref:
                data = doc.to_dict()
                data["id"] = doc.id
                all_data.append(data)

            return all_data
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")

    async def get_one_by_uid(self,uid_object: str):
        """
        Retrieve a document from the collection by its UID.

        This method searches for a document in the Firestore collection using the 
        provided UID. If the document exists, it returns its contents as a dictionary. 
        If the document does not exist, it raises a 404 HTTPException.

        Args:
            uid_object (str): The UID of the document to retrieve.

        Returns:
            dict: A dictionary representing the document data.

        Raises:
            HTTPException: If the document is not found (404) or an unexpected error occurs (500).
        """

        try:
            ref = self.collection.document(uid_object)
            docs = ref.get()
            if not docs.exists:
                raise HTTPException(status_code=404, detail= "file not found")
            return docs.to_dict()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def get_by_chapter(self, chapter_id: str):
        """
        Retrieve documents from the collection filtered by chapter ID.

        This method queries the Firestore collection for documents that match 
        the provided chapter ID. The results are returned as a dictionary 
        where each key is the document ID and the value is the document data.

        Args:
            chapter_id (str): The chapter ID used to filter the documents.

        Returns:
            dict: A dictionary with document IDs as keys and their data as values.

        Raises:
            HTTPException: If an unexpected error occurs during the query (500).
        """

        try:
            docs = self.collection.where(filter=FieldFilter("chapter_id", "==", chapter_id)).get()
            data = {doc.id: doc.to_dict() for doc in docs}
            return data
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def get_by_difficulty(self,difficulty: int):
        """
        Retrieve documents from the collection filtered by difficulty level.

        This method queries the Firestore collection for documents that match 
        the provided difficulty level. The results are returned as a dictionary 
        where each key is the document ID and the value is the document data.

        Args:
            difficulty (int): The difficulty level used to filter the documents.

        Returns:
            dict: A dictionary with document IDs as keys and their data as values.

        Raises:
            HTTPException: If an unexpected error occurs during the query (500).
        """

        try:
            docs = (self.collection.where(filter=FieldFilter("difficulty", "==", difficulty)).get())
            data = {doc.id: doc.to_dict() for doc in docs}
            return data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def get_by_categories(self,categories: str):
        """
        Retrieve documents from the collection filtered by category.

        This method queries the Firestore collection for documents where the 
        specified category is contained in the `categories` array field. The 
        results are returned as a dictionary where each key is the document ID 
        and the value is the document data.

        Args:
            categories (str): The category to search for within the `categories` array field.

        Returns:
            dict: A dictionary with document IDs as keys and their data as values.

        Raises:
            HTTPException: If an unexpected error occurs during the query (500).
        """

        try:
            docs = (self.collection.where(filter=FieldFilter("categories", "array_contains", categories)).get())
            data = {doc.id: doc.to_dict() for doc in docs}
            return data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def delete_by_id(self,document_uid: str):
        """
        Delete a document from the collection by its UID.

        This method deletes the document with the specified UID from the Firestore collection. 
        If the deletion is successful, it returns a confirmation message with the document ID.

        Args:
            document_uid (str): The UID of the document to delete.

        Returns:
            dict: A dictionary containing a confirmation message and the deleted document's ID.

        Raises:
            HTTPException: If an unexpected error occurs during the deletion (500).
        """

        try:
            self.collection.document(document_uid).delete()
            return {"message": "document delete", "id": document_uid}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def post_text(self,text: texts):
        """
        Add a new text document to the collection.

        This method adds a new document to the Firestore collection using the data 
        from the provided `text` object. It returns a confirmation message and the 
        UID of the newly created document.

        Args:
            text (texts): An instance of the `texts` model containing the data to be added.

        Returns:
            dict: A dictionary containing a confirmation message and the UID of the new document.

        Raises:
            HTTPException: If an unexpected error occurs during the document creation (500).
        """

        try:
            ref = self.collection.add(text.model_dump())
            return {"message": "post correct",
                    "uid": ref[1].id}  

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def update_url(self,chapter: str, url:str, segment:str):
        """
        Update the audio URL of documents matching a chapter and segment.

        This method searches for documents in the collection where the `audio_file` 
        matches the provided segment and the `chapter_id` matches the provided chapter. 
        It updates the `audio_url` field of all matching documents.

        Args:
            chapter (str): The chapter ID to filter documents.
            url (str): The new audio URL to set.
            segment (str): The audio file segment to filter documents.

        Returns:
            dict: A dictionary containing a confirmation message of the update.

        Raises:
            HTTPException: If no matching document is found (404) or if an unexpected 
            error occurs during the update (500).
        """

        try:
            query = self.collection\
                .where("audio_file", "==", segment)\
                .where("chapter_id", "==", chapter)
                
            results = query.stream()
                
            if not results:
                raise HTTPException(status_code= 404, detail="document not found")
                
            for doc in results:
                doc.reference.update({"audio_url": url})
                
            return {"message": "document update"}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def post_audio(self,file: UploadFile, chapter: str):
        """
        Upload an audio file to cloud storage and update its URL in the collection.

        This method uploads a `.flac` audio file to cloud storage under the specified 
        chapter folder. After uploading, it makes the file public and updates the 
        corresponding document's `audio_url` field in the collection.

        Args:
            file (UploadFile): The audio file to upload. Must be of type `.flac`.
            chapter (str): The chapter ID used to organize and update the audio URL.

        Returns:
            dict: A dictionary containing a confirmation message about the upload and URL update.

        Raises:
            HTTPException: If the file type is not supported or an unexpected error occurs during upload (500).
        """

        if file.content_type != "audio/flac":
            return {"error": "extension not suport"}
        
        try:
            content = await file.read()
            destination_path_cloud = f"corpus/{chapter}/{file.filename}"
            blob = storage.bucket().blob(destination_path_cloud)
            blob.upload_from_string(content, content_type= "audio/flac")
            blob.make_public()

            id = chapter
            segment = file.filename

            url_public = blob.public_url

            await self.update_url(chapter, url_public, segment)

            return {"message": "Audio and url update"}
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def update_evaluation(self, texts_evaluation: TextsEvaluation):
        """
        Update the audio analysis evaluation of documents matching a chapter and audio file.

        This method searches for documents in the collection where the `chapter_id` 
        and `audio_file` match the values provided in `texts_evaluation`. It updates 
        the `audio_analysis` field of all matching documents with the data from 
        `texts_evaluation`.

        Args:
            texts_evaluation (TextsEvaluation): An object containing the chapter ID, 
                audio file, and the audio analysis data to update.

        Returns:
            dict: A dictionary containing a confirmation message of the update.

        Raises:
            HTTPException: If no matching document is found (404) or if an unexpected 
            error occurs during the update (500).
        """

        try:

            query = self.collection.where("chapter_id","==", texts_evaluation.chapter_id)\
                                        .where("audio_file","==",texts_evaluation.audio_file)
            result = list(query.stream())

            if not result:
                raise HTTPException(status_code= 404, detail="document not found")
            
            for doc in result:
                doc.reference.update({
                    "audio_analysis": texts_evaluation.audio_analysis.model_dump()
                })
            
            return {"message": "document updated"}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def update_audio_duration(self, texts_audio_duration: TextsAudioDuration):
        """
        Update the audio duration of documents matching a chapter and audio file.

        This method searches for documents in the collection where the `chapter_id` 
        and `audio_file` match the values provided in `texts_audio_duration`. It updates 
        the `audio_duration` field of all matching documents.

        Args:
            texts_audio_duration (TextsAudioDuration): An object containing the chapter ID, 
                audio file, and the audio duration to update.

        Returns:
            dict: A dictionary containing a confirmation message of the update.

        Raises:
            HTTPException: If no matching document is found (404) or if an unexpected 
            error occurs during the update (500).
        """

        try:

            query = self.collection.where("chapter_id","==", texts_audio_duration.chapter_id)\
                                        .where("audio_file","==",texts_audio_duration.audio_file)
            result = list(query.stream())

            if not result:
                raise HTTPException(status_code= 404, detail="document not found")
            
            for doc in result:
                doc.reference.update({
                    "audio_duration": texts_audio_duration.audio_duration
                })
            
            return {"message": "document updated"}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")