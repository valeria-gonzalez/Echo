from app.db import db
from app.schemas.resourses_schemas import sentences, texts, words
from google.cloud.firestore_v1 import FieldFilter
from fastapi import HTTPException

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
    user_ref = db.collection("texts").document(text.id)
    user_ref.set(text.model_dump())
    return {"message": "text insert", "id": text.id}

async def post_words_service(word: words):
    user_ref = db.collection("words").document(word.id)
    user_ref.set(word.model_dump())
    return {"message": "word insert", "id": word.id}

async def post_sentences_service(sentence: sentences):
    user_ref = db.collection("sentences").document(str(sentence.id))
    user_ref.set(sentence.model_dump())
    return {"message": "sentence insert", "id": sentence.id}

