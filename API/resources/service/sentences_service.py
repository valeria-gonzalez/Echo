from app.db import db
from schemas.resources_schemas import sentences, SentencesEvaluation, SentencesAudioDuration
from google.cloud.firestore_v1 import FieldFilter
from fastapi import HTTPException, UploadFile
from firebase_admin import storage

class SentencesService():
    def __init__(self):
        self.collection = db.collection("sentences")

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
        
    async def get_by_audio_id(self, audio_id: int):
        try:
            docs = self.collection.where(filter=FieldFilter("audio_id", "==", audio_id)).get()
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
            self.collection.document(document_uid).delete()
            return {"message": "document delete", "id": document_uid}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def post_sentences(self,sentence: sentences):
        try:
            ref = self.collection.add(sentence.model_dump())
            return {"message": "post correct",
                    "uid": ref[1].id}  

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def update_url(self,id: int, url:str):
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