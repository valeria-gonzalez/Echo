from app.db import db
from schemas.resources_schemas import texts, TextsEvaluation, TextsAudioDuration
from google.cloud.firestore_v1 import FieldFilter
from fastapi import HTTPException, UploadFile
from firebase_admin import storage

class TextsService():
    def __init__(self):
        self.collection = db.collection("texts")

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
        
    async def get_by_chapter(self, chapter_id: str):
        try:
            docs = self.collection.where(filter=FieldFilter("chapter_id", "==", chapter_id)).get()
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
        
    async def post_text(self,text: texts):
        try:
            ref = self.collection.add(text.model_dump())
            return {"message": "post correct",
                    "uid": ref[1].id}  

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error {str(e)}")
        
    async def update_url(self,chapter: str, url:str, segment:str):
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