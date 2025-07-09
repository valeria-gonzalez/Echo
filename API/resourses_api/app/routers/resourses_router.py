from fastapi import APIRouter,HTTPException
from app.service.resourses_service import *
from app.schemas.resourses_schemas import texts, sentences, words

router = APIRouter(
    prefix="/resourses"
)

#get all 
@router.get("/texts")
async def get_texts_router():
    return get_texts_service()

@router.get("/sentences")
async def get_sentences_router():
    return get_sentences_service()

@router.get("/words")
async def get_words_router():
    return get_words_service()

#get by id

@router.get("/texts/{id}")
async def get_texts_id_router(id: int):
    return get_one_texts_service(id)

@router.get("/sentences/{id}")
async def get_sentences_id_router(id: int):
    return get_one_sentences_service(id)

@router.get("/words/{id}")	
async def get_words_id_router(id:int):
    return get_one_words_service(id)

#get by difficulty

@router.get("/texts/difficulty/{difficulty}")
async def get_texts_difficulty_router(id: int):
    return get_texts_difficulty_service(id)

@router.get("/sentences/difficulty/{difficulty}")
async def get_sentences_difficulty_router(id: int):
    return get_sentences_difficulty_service(id)

@router.get("/words/difficulty/{difficulty}")
async def get_words_difficulty_router(id: int):
    return get_words_difficulty_service(id)

#get by categories

@router.get("/texts/categories/{categories}")	
async def get_texts_categories_router(categories: str):
    return get_texts_categories_service(categories)

@router.get("/words/categories/{categories}")
async def get_words_categories_router(categories: str):
    return get_words_categories_service(categories)

@router.get("/sentences/categories/{categories}")	
async def get_sentences_categories_router(categories: str):
    return get_sentences_categories_service

#delete by id

@router.delete("/texts/{document_id}")
async def delete_texts_id_router(document_id: str):
    return delete_texts_id_service(document_id)

@router.delete("/words/{document_id}")
async def delete_words_id_router(document_id: str):
    return delete_words_id_service(document_id)

@router.delete("/sentences/{document_id}")
async def delete_sentences_id_router(document_id: str):
    return delete_sentences_id_service(document_id)

#post 

@router.post("/sentences")
async def post_sentence_router(sentence: sentences):
    return post_sentences_service(sentence)

@router.post("/texts")
async def post_texts_router(text: texts):
    return post_texts_service(text)

@router.post("/words")
async def post_words_router(word: words):
    return post_words_service(word)
