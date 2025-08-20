from app.db import db
from schemas.resources_schemas import words, WordsEvaluation, WordsAudioDuration
from google.cloud.firestore_v1 import FieldFilter
from fastapi import HTTPException, UploadFile
from firebase_admin import storage

class WordsService():
    def __init__(self):
        self.collection = db.collection("words")

    async def get_all(self):
        """
        Retrieves all documents from the Firestore collection.

        Returns:
            list[dict]: A list of dictionaries representing the documents in the collection.
                        Each dictionary contains the document data and an additional 'id' key 
                        corresponding to the document's ID.

        Raises:
            HTTPException: If an error occurs while fetching documents, raises a 500 status code 
                        with the error message.
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
        Retrieves a single document from the Firestore collection by its UID.

        Args:
            uid_object (str): The unique identifier of the document to retrieve.

        Returns:
            dict: A dictionary containing the document data.

        Raises:
            HTTPException: 
                404: If the document with the given UID does not exist.
                500: If an error occurs while fetching the document, with the error message.
        """
        try:
            ref = self.collection.document(uid_object)
            docs = ref.get()
            if not docs.exists:
                raise HTTPException(status_code=404, detail= "file not found")
            return docs.to_dict()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def get_by_text(self, text: str):
        """
        Retrieve documents from the collection that match the given text.

        This asynchronous method queries the collection using a filter on the "text" field.
        It returns a dictionary where the keys are document IDs and the values are the document data.

        Args:
            text (str): The text value to filter documents by.

        Returns:
            dict: A dictionary mapping document IDs to their corresponding data.

        Raises:
            HTTPException: If an error occurs during the retrieval process, an HTTP 500 error is raised with the exception details.
        """

        try:
            docs = self.collection.where(filter=FieldFilter("text", "==", text)).get()
            data = {doc.id: doc.to_dict() for doc in docs}
            return data
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def get_by_difficulty(self,difficulty: int):
        """
        Retrieve documents from the collection that match the specified difficulty level.

        This asynchronous method queries the collection using a filter on the "difficulty" field.
        It returns a dictionary where the keys are document IDs and the values are the document data.

        Args:
            difficulty (int): The difficulty level to filter documents by.

        Returns:
            dict: A dictionary mapping document IDs to their corresponding data.

        Raises:
            HTTPException: If an error occurs during the retrieval process, an HTTP 500 error is raised with the exception details.
        """

        try:
            docs = (self.collection.where(filter=FieldFilter("difficulty", "==", difficulty)).get())
            data = {doc.id: doc.to_dict() for doc in docs}
            return data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def get_by_categories(self,categories: str):
        """
        Retrieve documents from the collection that contain the specified category.

        This asynchronous method queries the collection using an "array_contains" filter on the "categories" field.
        It returns a dictionary where the keys are document IDs and the values are the document data.

        Args:
            categories (str): The category to filter documents by.

        Returns:
            dict: A dictionary mapping document IDs to their corresponding data.

        Raises:
            HTTPException: If an error occurs during the retrieval process, an HTTP 500 error is raised with the exception details.
        """

        try:
            docs = (self.collection.where(filter=FieldFilter("categories", "array_contains", categories)).get())
            data = {doc.id: doc.to_dict() for doc in docs}
            return data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        

    async def delete_by_id(self,document_uid: str):
        """
        Delete a document from the collection by its unique ID.

        This asynchronous method removes the document identified by `document_uid` from the collection.
        Upon successful deletion, it returns a confirmation message along with the deleted document's ID.

        Args:
            document_uid (str): The unique ID of the document to delete.

        Returns:
            dict: A dictionary containing a confirmation message and the deleted document's ID.

        Raises:
            HTTPException: If an error occurs during the deletion process, an HTTP 500 error is raised with the exception details.
        """

        try:
            db.self.collection.document(document_uid).delete()
            return {"message": "document delete", "id": document_uid}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        

    async def post_word(self,word: words):
        """
        Add a new word document to the collection.

        This asynchronous method inserts a new document into the collection using the provided `word` data.
        Upon successful insertion, it returns a confirmation message along with the unique ID of the created document.

        Args:
            word (words): The word object containing the data to be added to the collection.

        Returns:
            dict: A dictionary containing a confirmation message and the unique ID of the created document.

        Raises:
            HTTPException: If an error occurs during the insertion process, an HTTP 500 error is raised with the exception details.
        """

        try:
            ref = self.collection.add(word.model_dump())
            return {"message": "post correct",
                    "uid": ref[1].id} 

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def update_url(self,text: str, url:str):
        """
        Update the audio URL of a document by matching its text field.

        This asynchronous method searches for documents in the collection where the "text" field
        matches the given value. If one or more documents are found, their "audio_url" field is updated
        with the provided URL.

        Args:
            text (str): The text value used to identify the target document(s).
            url (str): The new audio URL to update in the document(s).

        Returns:
            dict: A dictionary containing a confirmation message when the update is successful.

        Raises:
            HTTPException:
                - 404: If no document is found matching the given text.
                - 500: If an unexpected error occurs during the update process.
        """

        try:
    
            query = self.collection.where("text", "==", text) 
            results = list(query.stream())
            
            if not results:
                raise HTTPException(status_code= 404, detail="document not found")
            
            for doc in results:
                doc.reference.update({"audio_url": url})
            
            return {"message": "document update"}
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def post_audio(self,file: UploadFile, text: str):
        """
        Upload an audio file to cloud storage and update its URL in the collection.

        This asynchronous method validates the uploaded file type, stores the file in cloud storage, 
        makes it publicly accessible, and updates the corresponding document's "audio_url" field 
        with the generated public URL.

        Args:
            file (UploadFile): The uploaded audio file to be stored.
            text (str): The text value used to identify the target document for updating the audio URL.

        Returns:
            dict: A dictionary containing a confirmation message when the audio is successfully uploaded 
            and the document URL is updated.

        Raises:
            HTTPException:
                - 500: If an unexpected error occurs during the upload or update process.
        """

        if file.content_type != "audio/mpeg":
            return {"error": "extension not suport"}
        
        try:
            content = await file.read()
            destination_path_cloud = f"wiki/{file.filename}"
            blob = storage.bucket().blob(destination_path_cloud)
            blob.upload_from_string(content, content_type= "audio/flac")
            blob.make_public()

            url_public = blob.public_url

            await self.update_url(text=text, url= url_public)

            return {"message": "Audio and url update"}
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def update_evaluation(self, words_evaluation: WordsEvaluation):
        """
        Update the audio analysis field of a document by matching its text field.

        This asynchronous method searches for documents in the collection where the "text" field
        matches the value provided in the `words_evaluation` object. If one or more documents are found,
        their "audio_analysis" field is updated with the given evaluation data.

        Args:
            words_evaluation (WordsEvaluation): An object containing the text identifier and the
                audio analysis data to update.

        Returns:
            dict: A dictionary containing a confirmation message when the update is successful.

        Raises:
            HTTPException:
                - 404: If no document is found matching the given text.
                - 500: If an unexpected error occurs during the update process.
        """


        try:

            query = self.collection.where("text","==", words_evaluation.text)
            result = list(query.stream())

            if not result:
                raise HTTPException(status_code= 404, detail="document not found")
            
            for doc in result:
                doc.reference.update({
                    "audio_analysis": words_evaluation.audio_analysis.model_dump()
                })
            
            return {"message": "document updated"}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def update_audio_duration(self, words_audio_duration: WordsAudioDuration):
        """
        Update the audio duration field of a document by matching its text field.

        This asynchronous method searches for documents in the collection where the "text" field
        matches the value provided in the `words_audio_duration` object. If one or more documents are found,
        their "audio_duration" field is updated with the given duration value.

        Args:
            words_audio_duration (WordsAudioDuration): An object containing the text identifier and the
                audio duration value to update.

        Returns:
            dict: A dictionary containing a confirmation message when the update is successful.

        Raises:
            HTTPException:
                - 404: If no document is found matching the given text.
                - 500: If an unexpected error occurs during the update process.
        """


        try:

            query = self.collection.where("text","==", words_audio_duration.text)
            result = list(query.stream())

            if not result:
                raise HTTPException(status_code= 404, detail="document not found")
            
            for doc in result:
                doc.reference.update({
                    "audio_duration": words_audio_duration.audio_duration
                })
            
            return {"message": "document updated"}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")