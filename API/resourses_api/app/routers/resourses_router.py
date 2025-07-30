from fastapi import APIRouter,HTTPException, UploadFile, File
from app.service.resourses_service import *
from app.schemas.resourses_schemas import texts, sentences, words, TextsEvaluation, SentencesEvaluation

router = APIRouter(
    prefix="/resources"
)

#get all 
@router.get("/texts")
async def get_texts_router():
    return await get_texts_service()

@router.get("/sentences")
async def get_sentences_router():
    return await get_sentences_service()

@router.get("/words")
async def get_words_router():
    return await get_words_service()

#get by id

@router.get("/texts/{id}")
async def get_texts_id_router(id: str):
    return await get_one_texts_service(id)

@router.get("/sentences/{id}")
async def get_sentences_id_router(id: str):
    return await get_one_sentences_service(id)

@router.get("/words/{id}")	
async def get_words_id_router(id:str):
    return await get_one_words_service(id)

#get by difficulty

@router.get("/texts/difficulty/{difficulty}")
async def get_texts_difficulty_router(id: int):
    return await get_texts_difficulty_service(id)

@router.get("/sentences/difficulty/{difficulty}")
async def get_sentences_difficulty_router(id: int):
    return await get_sentences_difficulty_service(id)

@router.get("/words/difficulty/{difficulty}")
async def get_words_difficulty_router(id: int):
    return await get_words_difficulty_service(id)

#get by categories

@router.get("/texts/categories/{categories}")	
async def get_texts_categories_router(categories: str):
    return await get_texts_categories_service(categories)

@router.get("/words/categories/{categories}")
async def get_words_categories_router(categories: str):
    return await get_words_categories_service(categories)

@router.get("/sentences/categories/{categories}")	
async def get_sentences_categories_router(categories: str):
    return await get_sentences_categories_service

#delete by id

@router.delete("/texts/{document_id}")
async def delete_texts_id_router(document_id: str):
    return await delete_texts_id_service(document_id)

@router.delete("/words/{document_id}")
async def delete_words_id_router(document_id: str):
    return await delete_words_id_service(document_id)

@router.delete("/sentences/{document_id}")
async def delete_sentences_id_router(document_id: str):
    return await delete_sentences_id_service(document_id)

#post 

@router.post("/sentences")
async def post_sentence_router(sentence: sentences):
    return await post_sentences_service(sentence)

@router.post("/texts")
async def post_texts_router(text: texts):
    return await post_texts_service(text)

@router.post("/words")
async def post_words_router(word: words):
    return await post_words_service(word)

@router.post("/sentences/audios")
async def post_sentences_audio_router(file: UploadFile = File(...)):
    return await post_audio_sentences_service(file)

@router.post("/texts/audios")
async def post_texts_audio_router(file: UploadFile = File(...), chapter: str = Form(...)):
    return await post_audio_texts_service(file,chapter)

@router.put("/texts/evaluation")
async def update_texts_evaluation_router(texts_evaluation: TextsEvaluation):
    return await update_evaluation_texts_service(texts_evaluation)

@router.put("/sentences/evaluation")
async def update_sentences_evaluation_router(sentences_evaluation: SentencesEvaluation):
    return await update_evaluation_sentences_service(sentences_evaluation)