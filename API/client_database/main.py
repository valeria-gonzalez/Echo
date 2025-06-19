#firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1 import FieldFilter
#fastapi
from fastapi import FastAPI

#pydantic
from pydantic import BaseModel

from datetime import datetime
from typing import List

from fastapi import HTTPException
# Use a service account.
cred = credentials.Certificate('echo-9f9e9-firebase-adminsdk-fbsvc-eb86b9ff51.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()


app = FastAPI()

class user(BaseModel):
    password: str
    name: str
    email: str
    id: str

@app.post("/users")
async def post_user(user: user):
    user_ref = db.collection("users").document(user.id)
    user_ref.set(user.model_dump())

class user_aplication(BaseModel):
    id: str
    creation_date: datetime
    last_login: datetime
    language: str

@app.post("/users_aplication")
async def post_user_aplication(user_aplication: user_aplication):
    user_ref = db.collection("user_aplication").document(user_aplication.id)
    user_ref.set(user_aplication.model_dump())

class user_data_profile(BaseModel):
    id: str
    profile_picture: str
    username: str

@app.post("/user_data_profile")
async def post_user_data_profile(user_data_profile: user_data_profile):
    user_ref = db.collection("user_data_profile").document(user_data_profile.id)
    user_ref.set(user_data_profile.model_dump())

class progress(BaseModel):
    id: str
    exercise_id: int
    complet: int
    attempts: int
    situation: str
    type: str
    completion_date: datetime
    last_attempt: datetime

@app.post("/progress")
async def post_progress(progress: progress):
    user_ref = db.collection("progress").document(progress.id)
    user_ref.set(progress.model_dump())

class additional_information(BaseModel):
    id: str
    data_of_birth: datetime
    gender: int

@app.post("/additional_information")
async def post_additional_information(additional_information: additional_information):
    user_ref = db.collection("additional_information").document(additional_information.id)
    user_ref.set(additional_information.model_dump())

class Calificacion(BaseModel):
    overall_rating: int
    clarity_rating: int
    speed_rating: int
    tone_rating: int
    phonetic_rating: int

class Tips(BaseModel):
    clarity_tip: str
    speed_tip: str
    phonetic_tip: str
    tone_tip: str

class evaluation(BaseModel):
    id: str
    exercise_id: int
    evaluation: int
    type: str
    user_recoring_link: str
    calificacion: Calificacion
    tips: Tips

@app.post("/evaluation")
async def post_evaluation(evaluation: evaluation):
    user_ref = db.collection("evaluation").document(evaluation.id)
    user_ref.set(evaluation.model_dump())

class Transcript(BaseModel):
    audio_file: str
    duration: float
    full_text: str
    text_lines: List[str]

class text(BaseModel):
    id: str
    #text_id: int
    chapter_id: str
    book_title: str

    transcript: Transcript

    difficulty: int
    categories: List[str]
    #word_count: int

@app.post("/text")
async def post_text(text: text):
    user_ref = db.collection("texts").document(text.id)
    user_ref.set(text.model_dump())

class DefinitionsIn(BaseModel):
    pos: str
    definitions: List[str]

class words(BaseModel):
    id: str
    definitions: List[DefinitionsIn]
    ipa: str
    mp3_url: str
    translations: list[str]
    categories: list[str]
    difficulty: int

@app.post("/words")
async def post_words(words: words):
    user_ref = db.collection("words").document(words.id)
    user_ref.set(words.model_dump())

class sentences(BaseModel):
    id: int
    #sentences_id: int
    eng_sen: str
    spa_sen: str
    audio_id: int
    #duration: int
    categories: List[str]
    difficulty: int


@app.post("/sentences")
async def post_sentences(sentences: sentences):
    user_ref = db.collection("sentences").document(str(sentences.id))
    user_ref.set(sentences.model_dump())

#getall
@app.get("/getall/{collection_name}")
async def get_all(collection_name: str):
    ref = db.collection(collection_name)
    docs = ref.stream()
    allcoletion = []

    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        allcoletion.append(data)
    
    return allcoletion

#getall
@app.get("/{collection_name}/{id_object}")
async def get_all(collection_name: str,id_object):
    ref = db.collection(collection_name).document(id_object)
    docs = ref.get()
    if not docs.exists:
        raise HTTPException(status_code=404, detail= "file not found")
        
    return docs.to_dict()

#deleteDocument
@app.delete("/delete/{colection_name}/{document_id}")
async def delete_document(colection_name: str, document_id: str):
    db.collection(colection_name).document(document_id).delete()


#GET text_difficulty_list {difficulty}: Returns a list of text information that have a specific difficulty.
#GET sentence_difficulty_list {difficulty}: Returns a list of sentence information that have a specific difficulty.
#GET word_difficulty_list {difficulty}: Returns a list of word information that have a specific difficulty.

@app.get("/{collection_name}/difficulty/{difficulty}")
async def get_sentences_difficulty(collection_name: str, difficulty: int):
    docs = (db.collection(collection_name).where(filter=FieldFilter("difficulty", "==", difficulty)).get())
    data = {doc.id: doc.to_dict() for doc in docs}
    return data

#GET text_category_list {category}: Returns a list of texts information that have a specific category.
#GET sentence_category_list {category}: Returns a list of sentence information that have a specific category.
#GET word_category_list {category}: Returns a list of word information that have a specific category.
@app.get("/{collection_name}/categories/{categories}")
async def get_collection_difficulty(collection_name: str, categories: str):
    docs = (db.collection(collection_name).where(filter=FieldFilter("categories", "array_contains", categories)).get())
    data = {doc.id: doc.to_dict() for doc in docs}
    return data
