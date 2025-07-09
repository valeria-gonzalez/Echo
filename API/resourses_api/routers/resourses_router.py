from fastapi import APIRouter,HTTPException
from routers.resourses_router import router
from service.resourses_service import *
from schemas.resourses_schemas import texts, sentences, words

router = APIRouter(
    prefix="/resourses"
)

@router.get("/texts/{id}")
async def get_texts_id(int: id):
    return get_one_text(id)

@router.get("/sentences/{id}")
async def get_sentences_id(int: id):
    return get_one_sentences(id)

@router.get("/words/{id}")	
async def get_words_id(int: id):
    return get_one_words(id)

@router.get("/texts/difficulty/{difficulty}")	
@router.get("/sentences/difficulty/{difficulty}")	
@router.get("/words/difficulty/{difficulty}")	

@router.get("/texts/categories/{categories}")	
@router.get("/words/categories/{categories}")	
@router.get("/sentences/categories/{categories}")	

@router.delete("/texts/{document_id}")
@router.delete("/words/{document_id}")
@router.delete("/sentences/{document_id}")

@router.post("/sentences")
@router.post("/texts")
@router.post("/words")
