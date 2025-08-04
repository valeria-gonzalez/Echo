from app.db import db
from schemas.resources_schemas import words, WordsEvaluation
from google.cloud.firestore_v1 import FieldFilter
from fastapi import HTTPException, UploadFile
from firebase_admin import storage

class WordsService():
    """Service for words related operations in the Firestore database."""
    def __init__(self):
        self.collection = db.collection("words")

    async def get_all(self):
        """
        Get all coleccions about the collection words

        Returns:
            all_data(List(dic)) : List with all the words data

        Raises:
            HttpEXception: If an error occurs
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
        Get the information about the collection words with specific id

        Args:

            uid_object(str): id word we want the information

        Returns:
            return collection with the uid

        Raises:
            HttpEXception: If an error occurs
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
        Get the information about the collection words with specific text

        Args:

            text(str): text word we want the information

        Returns:
            return collection with the text

        Raises:
            HttpEXception: If an error occurs
        """
        try:
            docs = self.collection.where(filter=FieldFilter("text", "==", text)).get()
            data = {doc.id: doc.to_dict() for doc in docs}
            return data
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def get_by_difficulty(self,difficulty: int):
        """
        Get the information about the collection  with specific difficulty

        Args:

            difficulty(int): difficulty we want to get

        Returns:
            return collection with the collections with the same difficulty

        Raises:
            HttpEXception: If an error occurs
        """
        try:
            docs = (self.collection.where(filter=FieldFilter("difficulty", "==", difficulty)).get())
            data = {doc.id: doc.to_dict() for doc in docs}
            return data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def get_by_categories(self,categories: str):
        """
        Get the information about the collection  with specific categories

        Args:

            categories(str): categories we want to get

        Returns:
            return collection with the collections with the same categories

        Raises:
            HttpEXception: If an error occurs
        """
        try:
            docs = (self.collection.where(filter=FieldFilter("categories", "array_contains", categories)).get())
            data = {doc.id: doc.to_dict() for doc in docs}
            return data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        

    async def delete_by_id(self,document_uid: str):
        """
        Delete the  collection with the document_uid

        Args:

            document_id(str): string with the uid

        Returns:
            return message with the followin text "document delete"

        Raises:
            HttpEXception: If an error occurs
        """
        try:
            db.self.collection.document(document_uid).delete()
            return {"message": "document delete", "id": document_uid}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        

    async def post_word(self,word: words):
        """
        Insert a new word into the 'words' collection.

        Args:
            word (words): Word object based on the Pydantic schema.

        Returns:
            dict: A message with the ID of the newly created document.

        Raises:
            HTTPException: If an error occurs during the operation.
        """
        try:
            ref = self.collection.add(word.model_dump())
            return {"message": "post correct",
                    "uid": ref[1].id} 

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def update_url(self,text: str, url:str):
        """
        Update the 'audio_url' field in documents from the 'words' collection
        where the 'text' matches the given text.

        Args:
            text (str): id sentences we want to change
            url(str): url we want to add to the collection

        Returns:
            message: "the document update"

        Raises:
            HTTPException: If an error occurs during the operation.
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
        Upload an audio file to Google Cloud Storage and update its public URL in the Firestore database.

        Args:
            file (UploadFile): The audio file uploaded
            text (str): The word we want change

        Returns:
            dict: A success message and the public URL of the uploaded audio.

        Raises:
            HTTPException:

        """
        if file.content_type != "audio/flac":
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
        Update the 'audio_analysis' field of a document in the Firestore collection,
        identified by its 'text'.

        Args:
            sentences_evaluation (SentencesEvaluation): An object containing the text
                and the audio_analysis data to be updated.

        Returns:
            dict: Message indicating the update result.

        Raises:
            HTTPException:
        """

        try:

            query = self.collection.where("text","==", words_evaluation.text)\
                                        .where("audio_file","==",words_evaluation.audio_file)
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