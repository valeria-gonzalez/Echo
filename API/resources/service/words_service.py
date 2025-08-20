from app.db import db
from schemas.resources_schemas import words, WordsEvaluation, WordsAudioDuration
from google.cloud.firestore_v1 import FieldFilter
from fastapi import HTTPException, UploadFile
from firebase_admin import storage

class WordsService():
    """Service for words related operations in the Firestore database."""
    def __init__(self):
        self.collection = db.collection("words")

    async def get_all(self):
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
        try:
            ref = self.collection.document(uid_object)
            docs = ref.get()
            if not docs.exists:
                raise HTTPException(status_code=404, detail= "file not found")
            return docs.to_dict()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def get_by_text(self, text: str):
        try:
            docs = self.collection.where(filter=FieldFilter("text", "==", text)).get()
            data = {doc.id: doc.to_dict() for doc in docs}
            return data
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def get_by_difficulty(self,difficulty: int):
        try:
            docs = (self.collection.where(filter=FieldFilter("difficulty", "==", difficulty)).get())
            data = {doc.id: doc.to_dict() for doc in docs}
            return data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def get_by_categories(self,categories: str):
        try:
            docs = (self.collection.where(filter=FieldFilter("categories", "array_contains", categories)).get())
            data = {doc.id: doc.to_dict() for doc in docs}
            return data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        

    async def delete_by_id(self,document_uid: str):
        try:
            db.self.collection.document(document_uid).delete()
            return {"message": "document delete", "id": document_uid}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        

    async def post_word(self,word: words):
        try:
            ref = self.collection.add(word.model_dump())
            return {"message": "post correct",
                    "uid": ref[1].id} 

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def update_url(self,text: str, url:str):
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