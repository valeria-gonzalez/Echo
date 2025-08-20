from fastapi import APIRouter,HTTPException, UploadFile, File, Form

from service.sentences_service import SentencesService
from service.texts_service import TextsService
from service.words_service import WordsService

from schemas.resources_schemas import words, texts, sentences, WordsEvaluation , TextsEvaluation , SentencesEvaluation, TextsAudioDuration, SentencesAudioDuration, WordsAudioDuration
router = APIRouter(
    prefix="/resources",
    tags=["Information about resurces"],
)

texts_service = TextsService()
sentences_service = SentencesService()
words_service = WordsService()

#get all 
@router.get("/texts")
async def get_texts_router():
    try:
        return await texts_service.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/sentences")
async def get_sentences_router():
    try:
        return await sentences_service.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
@router.get("/words")
async def get_words_router():
    try:
        return await words_service.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

#get by uid

@router.get("/texts/{id}")
async def get_texts_id_router(id: str):
    try:
        return await texts_service.get_one_by_uid(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/sentences/{id}")
async def get_sentences_id_router(id: str):
    try:
        return await sentences_service.get_one_by_uid(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/words/{id}")	
async def get_words_id_router(id:str):
    try:
        return await words_service.get_one_by_uid(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

#get by id

@router.get("/texts/chapter/{id}")
async def get_texts_id_router(id: str):
    try:
        return await texts_service.get_by_chapter(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/sentences/audio_id/{id}")
async def get_sentences_id_router(id: int):
    try:
        return await sentences_service.get_by_audio_id(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/words/text/{id}")	
async def get_words_id_router(id:str):
    try:
        return await words_service.get_by_text(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

#get by difficulty

@router.get("/texts/difficulty/{difficulty}")
async def get_texts_difficulty_router(difficulty: int):
    try:
        return await texts_service.get_by_difficulty(difficulty)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/sentences/difficulty/{difficulty}")
async def get_sentences_difficulty_router(difficulty: int):
    try:
        return await sentences_service.get_by_difficulty(difficulty)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/words/difficulty/{difficulty}")
async def get_words_difficulty_router(difficulty: int):
    try:
        return await words_service.get_by_difficulty(difficulty)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

#get by categories

@router.get("/texts/categories/{categories}")	
async def get_texts_categories_router(categories: str):
    try:
        return await texts_service.get_by_categories(categories)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/words/categories/{categories}")
async def get_words_categories_router(categories: str):
    try:
        return await words_service.get_by_categories(categories)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/sentences/categories/{categories}")	
async def get_sentences_categories_router(categories: str):
    try:
        return await sentences_service.get_by_categories(categories)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

#delete by id

@router.delete("/texts/{document_id}")
async def delete_texts_id_router(document_id: str):
    try:
        return await texts_service.delete_by_id(document_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.delete("/words/{document_id}")
async def delete_words_id_router(document_id: str):
    try:
        return await words_service.delete_by_id(document_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.delete("/sentences/{document_id}")
async def delete_sentences_id_router(document_id: str):
    try:
        return await sentences_service.delete_by_id(document_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

#post texts. words, sentences

@router.post("/sentences")
async def post_sentence_router(sentence: sentences):
    try:
        return await sentences_service.post_sentences(sentence)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.post("/texts")
async def post_texts_router(text: texts):
    try:
        return await texts_service.post_text(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.post("/words")
async def post_words_router(word: words):
    try:
        return await words_service.post_word(word)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

#post audio
@router.post("/sentences/audios")
async def post_sentences_audio_router(file: UploadFile = File(...)):
    try:
        return await sentences_service.post_audio(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.post("/texts/audios")
async def post_texts_audio_router(file: UploadFile = File(...), chapter: str = Form(...)):
    try:
        return await texts_service.post_audio(file=file, chapter=chapter)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.post("/words/audios")
async def post_words_audio_router(file: UploadFile = File(...), text: str = Form(...)):
    try:
        return await words_service.post_audio(file= file, text= text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

#update evaluation
@router.put("/texts/evaluation")
async def update_texts_evaluation_router(texts_evaluation: TextsEvaluation):
    try:
        return await texts_service.update_evaluation(texts_evaluation=texts_evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.put("/sentences/evaluation")
async def update_sentences_evaluation_router(sentences_evaluation: SentencesEvaluation):
    try:
        return await sentences_service.update_evaluation(sentences_evaluation=sentences_evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.put("/words/evaluation")
async def update_words_evaluation_router(words_evaluation: WordsEvaluation):
    try:
        return await words_service.update_evaluation(words_evaluation=words_evaluation)    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

#update audio_duration
@router.put("/texts/audio_duration")
async def update_texts_audio_duration_router(texts_audio_duration: TextsAudioDuration):
    try:
        return await texts_service.update_audio_duration(texts_audio_duration=texts_audio_duration)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
@router.put("/sentences/audio_duration")
async def update_sentences_audio_duration_router(sentences_audio_duration: SentencesAudioDuration):
    try:
        return await sentences_service.update_audio_duration(sentences_audio_duration=sentences_audio_duration)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
@router.put("/words/audio_duration")
async def update_words_audio_duration_router(words_audio_duration: WordsAudioDuration):
    try:
        return await words_service.update_audio_duration(words_audio_duration=words_audio_duration)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")