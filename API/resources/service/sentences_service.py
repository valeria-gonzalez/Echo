from app.db import db
from schemas.resources_schemas import sentences, SentencesEvaluation, SentencesAudioDuration
from google.cloud.firestore_v1 import FieldFilter
from fastapi import HTTPException, UploadFile
from firebase_admin import storage

class SentencesService():
    def __init__(self):
        self.collection = db.collection("sentences")

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
        
    async def get_by_audio_id(self, audio_id: int):
        """
        Retrieves documents from the Firestore collection that match a specific audio ID.

        Args:
            audio_id (int): The audio ID to filter documents by.

        Returns:
            dict: A dictionary where each key is a document ID and the value is the corresponding 
                document data.

        Raises:
            HTTPException: 
                500: If an error occurs while fetching documents, with the error message.
        """
        try:
            docs = self.collection.where(filter=FieldFilter("audio_id", "==", audio_id)).get()
            data = {doc.id: doc.to_dict() for doc in docs}
            return data
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def get_by_difficulty(self,difficulty: int):
        """
        Retrieves documents from the Firestore collection that match a specific difficulty level.

        Args:
            difficulty (int): The difficulty level to filter documents by.

        Returns:
            dict: A dictionary where each key is a document ID and the value is the corresponding 
                document data.

        Raises:
            HTTPException:
                500: If an error occurs while fetching documents, with the error message.
        """
        try:
            docs = (self.collection.where(filter=FieldFilter("difficulty", "==", difficulty)).get())
            data = {doc.id: doc.to_dict() for doc in docs}
            return data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def get_by_categories(self,categories: str):
        """
        Retrieves documents from the Firestore collection that contain a specific category.

        Args:
            categories (str): The category to filter documents by.

        Returns:
            dict: A dictionary where each key is a document ID and the value is the corresponding
                document data.

        Raises:
            HTTPException:
                500: If an error occurs while fetching documents, with the error message.
        """
        try:
            docs = (self.collection.where(filter=FieldFilter("categories", "array_contains", categories)).get())
            data = {doc.id: doc.to_dict() for doc in docs}
            return data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def delete_by_id(self,document_uid: str):
        """
        Deletes a document from the Firestore collection by its UID.

        Args:
            document_uid (str): The unique identifier of the document to delete.

        Returns:
            dict: A confirmation message containing the deleted document's ID.

        Raises:
            HTTPException:
                500: If an error occurs while deleting the document, with the error message.
        """
        try:
            self.collection.document(document_uid).delete()
            return {"message": "document delete", "id": document_uid}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def post_sentences(self,sentence: sentences):
        """
        Adds a new sentence document to the Firestore collection.

        Args:
            sentence (sentences): An instance of the `sentences` model containing the data 
                                to store.

        Returns:
            dict: A confirmation message with the newly created document's UID.

        Raises:
            HTTPException:
                500: If an error occurs while adding the document, with the error message.
        """
        try:
            ref = self.collection.add(sentence.model_dump())
            return {"message": "post correct",
                    "uid": ref[1].id}  

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def update_url(self,id: int, url:str):
        """
        Updates the audio URL of documents in the Firestore collection that match a specific audio ID.

        Args:
            id (int): The audio ID to identify which documents to update.
            url (str): The new URL to set for the 'audio_url' field.

        Returns:
            dict: A confirmation message indicating the document(s) were updated.

        Raises:
            HTTPException:
                404: If no documents with the given audio ID are found.
                500: If an error occurs while updating the document(s), with the error message.
        """
        try:
    
            query = self.collection.where("audio_id", "==", id) 
            results = list(query.stream())
            
            if not results:
                raise HTTPException(status_code= 404, detail="document not found")
            
            for doc in results:
                doc.reference.update({"audio_url": url})
            
            return {"message": "document update"}
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def post_audio(self, file: UploadFile):
        """
        Uploads an audio file to cloud storage and updates the corresponding document's URL in Firestore.

        Args:
            file (UploadFile): The audio file to upload. Must be in MP3 format.

        Returns:
            dict: A message confirming the audio upload and URL update, or an error message 
                if the file format is unsupported.

        Raises:
            HTTPException:
                500: If an error occurs during the upload or Firestore update, with the error message.
        """
        if file.content_type != "audio/mpeg":
            return {"error": "extension not supported"}
        
        try:
            content = await file.read()
            destination_path_cloud = f"tatoeba/{file.filename}"
            blob = storage.bucket().blob(destination_path_cloud)
            blob.upload_from_string(content, content_type= "audio/mpeg")
            blob.make_public()
            id = int(file.filename.removesuffix(".mp3"))
            url_public = blob.public_url

            await self.update_url(id, url_public)

            return {"message": "Audio and url update"}
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
            
    async def update_evaluation(self, sentences_evaluation: SentencesEvaluation):
        """
        Updates the evaluation data of documents in the Firestore collection that match a specific audio ID.

        Args:
            sentences_evaluation (SentencesEvaluation): An instance containing the audio ID and 
                                                        the evaluation data to update.

        Returns:
            dict: A confirmation message indicating the document(s) were updated.

        Raises:
            HTTPException:
                404: If no documents with the given audio ID are found.
                500: If an error occurs while updating the document(s), with the error message.
        """

        try:

            query = self.collection.where("audio_id","==", sentences_evaluation.audio_id)
            result = list(query.stream())

            if not result:
                raise HTTPException(status_code= 404, detail="document not found")
            
            for doc in result:
                doc.reference.update({
                    "audio_analysis": sentences_evaluation.audio_analysis.model_dump()
                })
            
            return {"message": "document updated"}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def update_audio_duration(self, sentences_audio_duration: SentencesAudioDuration):
        """
        Updates the audio duration of documents in the Firestore collection that match a specific audio ID.

        Args:
            sentences_audio_duration (SentencesAudioDuration): An instance containing the audio ID 
                                                                and the new audio duration.

        Returns:
            dict: A confirmation message indicating the document(s) were updated.

        Raises:
            HTTPException:
                404: If no documents with the given audio ID are found.
                500: If an error occurs while updating the document(s), with the error message.
        """

        try:
            query = self.collection.where("audio_id","==", sentences_audio_duration.audio_id)
            result = list(query.stream())

            if not result:
                raise HTTPException(status_code= 404, detail="document not found")
            
            for doc in result:
                doc.reference.update({
                    "audio_duration": sentences_audio_duration.audio_duration
                })
            
            return {"message": "document updated"}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")