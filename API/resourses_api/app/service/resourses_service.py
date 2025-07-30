from app.db import db, bucket
from app.schemas.resourses_schemas import sentences, texts, words, TextsEvaluation, SentencesEvaluation
from google.cloud.firestore_v1 import FieldFilter
from fastapi import HTTPException, UploadFile, Form
from firebase_admin import storage


#get all
async def get_sentences_service():
    ref = db.collection("sentences")
    docs = ref.stream()
    allcoletion = []

    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        allcoletion.append(data)
    
    return allcoletion


async def get_texts_service():
    ref = db.collection("texts")
    docs = ref.stream()
    allcoletion = []

    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        allcoletion.append(data)
    
    return allcoletion

async def get_words_service():
    ref = db.collection("words")
    docs = ref.stream()
    allcoletion = []

    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        allcoletion.append(data)
    
    return allcoletion

#get one by id
async def get_one_texts_service(id_object: int):
    ref = db.collection("texts").document(id_object)
    docs = ref.get()
    if not docs.exists:
        
        raise HTTPException(status_code=404, detail= "file not found")
        
    return docs.to_dict()

async def get_one_sentences_service(id_object: int):
    ref = db.collection("sentences").document(id_object)
    docs = ref.get()
    if not docs.exists:
        raise HTTPException(status_code=404, detail= "file not found")
        
    return docs.to_dict()

async def get_one_words_service(id_object: int):
    ref = db.collection("words").document(id_object)
    docs = ref.get()
    if not docs.exists:
        raise HTTPException(status_code=404, detail= "file not found")
        
    return docs.to_dict()

#get by difficulty
async def get_sentences_difficulty_service(difficulty: int):
    docs = (db.collection("sentences").where(filter=FieldFilter("difficulty", "==", difficulty)).get())
    data = {doc.id: doc.to_dict() for doc in docs}
    return data

async def get_texts_difficulty_service(difficulty: int):
    docs = (db.collection("texts").where(filter=FieldFilter("difficulty", "==", difficulty)).get())
    data = {doc.id: doc.to_dict() for doc in docs}
    return data

async def get_words_difficulty_service(difficulty: int):
    docs = (db.collection("words").where(filter=FieldFilter("difficulty", "==", difficulty)).get())
    data = {doc.id: doc.to_dict() for doc in docs}
    return data

#get by categories
async def get_texts_categories_service(categories: str):
    docs = (db.collection("texts").where(filter=FieldFilter("categories", "array_contains", categories)).get())
    data = {doc.id: doc.to_dict() for doc in docs}
    return data

async def get_sentences_categories_service(categories: str):
    docs = (db.collection("sentences").where(filter=FieldFilter("categories", "array_contains", categories)).get())
    data = {doc.id: doc.to_dict() for doc in docs}
    return data

async def get_words_categories_service(categories: str):
    docs = (db.collection("words").where(filter=FieldFilter("categories", "array_contains", categories)).get())
    data = {doc.id: doc.to_dict() for doc in docs}
    return data

#delete by id
async def delete_texts_id_service(document_id: str):
    db.collection("texts").document(document_id).delete()
    return {"message": "document delete", "id": document_id}

async def delete_words_id_service(document_id: str):
    db.collection("words").document(document_id).delete()
    return {"message": "document delete", "id": document_id}

async def delete_sentences_id_service(document_id: str):
    db.collection("sentences").document(document_id).delete()
    return {"message": "document delete", "id": document_id}

#post 
async def post_texts_service(text: texts):
    user_ref = db.collection("texts").add(text.model_dump())
    return {"message": "text insert"}

async def post_words_service(word: words):
    user_ref = db.collection("words").add(word.model_dump())
    return {"message": "word insert"}

async def post_sentences_service(sentence: sentences):
    user_ref = db.collection("sentences").add(sentence.model_dump())
    return {"message": "sentence insert"}

#UPDATE
async def update_sentences_url_service(id: int, url:str):

    query = db.collection("sentences").where("audio_id", "==", id) 
    results = query.stream()
    
    if not results:
        raise HTTPException(status_code= 404, detail="document not found")
    
    for doc in results:
        doc.reference.update({"audio_url": url})
    
    return {"message": "document update"}

async def update_texts_url_service(chapter: str, url:str, segment:str):

    query = db.collection("texts")\
        .where("audio_file", "==", segment)\
        .where("chapter_id", "==", chapter)
    
    results = query.stream()
    
    if not results:
        raise HTTPException(status_code= 404, detail="document not found")
    
    for doc in results:
        doc.reference.update({"audio_url": url})
    
    return {"message": "document update"}

#POST AUDIO sentences

async def post_audio_sentences_service(file: UploadFile):
    if file.content_type != "audio/mpeg":
        return {"error": "extension not suport"}
    
    try:
        content = await file.read()
        destination_path_cloud = f"tatoeba/{file.filename}"
        blob = storage.bucket().blob(destination_path_cloud)
        blob.upload_from_string(content, content_type= "audio/mpeg")
        blob.make_public()
        id = int(file.filename.removesuffix(".mp3"))
        url_public = blob.public_url

        await update_sentences_url_service(id, url_public)

        return {"message": "Audio and url update"}

    except Exception as e:
        return {"error": str(e)}
    
#POST AUDIO texts

async def post_audio_texts_service(file: UploadFile, chapter: str):
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

        await update_texts_url_service(chapter, url_public, segment)

        return {"message": "Audio and url update"}

    except Exception as e:
        return {"error": str(e)}
    
async def update_evaluation_sentences_service(sentences_evaluation: SentencesEvaluation):

    query = db.collection("sentences").where("audio_id","==", sentences_evaluation.audio_id)
    result = query.stream()

    if not result:
        raise HTTPException(status_code= 404, detail="document not found")
    
    for doc in result:
        doc.reference.update({"audio_analysis": sentences_evaluation.audio_analysis.model_dump()})
    
    return {"message": "document update"}

async def update_evaluation_texts_service(texts_evaluation: TextsEvaluation):
    
    query = db.collection("texts").where("chapter_id","==", texts_evaluation.chapter_id)\
                                        .where("audio_file","==",texts_evaluation.audio_file)
    result = query.stream()

    if not result:
        raise HTTPException(status_code= 404, detail="document not found")
    
    for doc in result:
        doc.reference.update({"audio_analysis": texts_evaluation.audio_analysis.model_dump()})
    
    return {"message": "document update"}