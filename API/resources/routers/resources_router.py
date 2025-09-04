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

@router.get("/texts")
async def get_texts_router():
    """
    Retrieve all text documents.

    This endpoint returns a list of all text documents from the texts collection.

    Returns:
        list[dict]: A list of dictionaries, each representing a text document.

    Raises:
        HTTPException: If an unexpected error occurs during retrieval (500).
    """
    try:
        return await texts_service.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/sentences")
async def get_sentences_router():
    """
    Retrieve all sentence documents.

    This endpoint returns a list of all sentence documents from the sentences collection.

    Returns:
        list[dict]: A list of dictionaries, each representing a sentence document.

    Raises:
        HTTPException: If an unexpected error occurs during retrieval (500).
    """
    try:
        return await sentences_service.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
@router.get("/words")
async def get_words_router():
    """
    Retrieve all word documents.

    This endpoint returns a list of all word documents from the words collection.

    Returns:
        list[dict]: A list of dictionaries, each representing a word document.

    Raises:
        HTTPException: If an unexpected error occurs during retrieval (500).
    """
    try:
        return await words_service.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

#get by uid

@router.get("/texts/{id}")
async def get_texts_id_router(id: str):
    """
    Retrieve a text document by its UID.

    This endpoint fetches a single text document from the texts collection 
    using the provided unique ID.

    Args:
        id (str): The UID of the text document to retrieve.

    Returns:
        dict: A dictionary representing the text document.

    Raises:
        HTTPException: If the document is not found or an unexpected error occurs (500).
    """
    try:
        return await texts_service.get_one_by_uid(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/sentences/{id}")
async def get_sentences_id_router(id: str):
    """
    Retrieve a sentence document by its UID.

    This endpoint fetches a single sentence document from the sentences collection 
    using the provided unique ID.

    Args:
        id (str): The UID of the sentence document to retrieve.

    Returns:
        dict: A dictionary representing the sentence document.

    Raises:
        HTTPException: If the document is not found or an unexpected error occurs (500).
    """
    try:
        return await sentences_service.get_one_by_uid(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/words/{id}")	
async def get_words_id_router(id:str):
    """
    Retrieve a word document by its UID.

    This endpoint fetches a single word document from the words collection 
    using the provided unique ID.

    Args:
        id (str): The UID of the word document to retrieve.

    Returns:
        dict: A dictionary representing the word document.

    Raises:
        HTTPException: If the document is not found or an unexpected error occurs (500).
    """
    try:
        return await words_service.get_one_by_uid(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

#get by id

@router.get("/texts/chapter/{id}")
async def get_texts_id_router(id: str):
    """
    Retrieve text documents by chapter ID.

    This endpoint fetches all text documents that belong to the specified chapter.

    Args:
        id (str): The chapter ID to filter text documents.

    Returns:
        dict: A dictionary where each key is a document ID and the value is the document data.

    Raises:
        HTTPException: If an unexpected error occurs during retrieval (500).
    """
    try:
        return await texts_service.get_by_chapter(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/sentences/audio_id/{id}")
async def get_sentences_id_router(id: int):
    """
    Retrieve sentence documents by audio ID.

    This endpoint fetches all sentence documents that are associated with the specified audio ID.

    Args:
        id (int): The audio ID to filter sentence documents.

    Returns:
        dict: A dictionary where each key is a document ID and the value is the document data.

    Raises:
        HTTPException: If an unexpected error occurs during retrieval (500).
    """
    try:
        return await sentences_service.get_by_audio_id(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/words/text/{id}")	
async def get_words_id_router(id:str):
    """
    Retrieve word documents by text.

    This endpoint fetches all word documents that match the specified text.

    Args:
        id (str): The text used to filter word documents.

    Returns:
        dict: A dictionary where each key is a document ID and the value is the document data.

    Raises:
        HTTPException: If an unexpected error occurs during retrieval (500).
    """
    try:
        return await words_service.get_by_text(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

#get by difficulty

@router.get("/texts/difficulty/{difficulty}")
async def get_texts_difficulty_router(difficulty: int):
    """
    Retrieve text documents filtered by difficulty level.

    This endpoint fetches all text documents that match the specified difficulty.

    Args:
        difficulty (int): The difficulty level used to filter text documents.

    Returns:
        dict: A dictionary where each key is a document ID and the value is the document data.

    Raises:
        HTTPException: If an unexpected error occurs during retrieval (500).
    """
    try:
        return await texts_service.get_by_difficulty(difficulty)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/sentences/difficulty/{difficulty}")
async def get_sentences_difficulty_router(difficulty: int):
    """
    Retrieve sentence documents filtered by difficulty level.

    This endpoint fetches all sentence documents that match the specified difficulty.

    Args:
        difficulty (int): The difficulty level used to filter sentence documents.

    Returns:
        dict: A dictionary where each key is a document ID and the value is the document data.

    Raises:
        HTTPException: If an unexpected error occurs during retrieval (500).
    """
    try:
        return await sentences_service.get_by_difficulty(difficulty)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/words/difficulty/{difficulty}")
async def get_words_difficulty_router(difficulty: int):
    """
    Retrieve word documents filtered by difficulty level.

    This endpoint fetches all word documents that match the specified difficulty.

    Args:
        difficulty (int): The difficulty level used to filter word documents.

    Returns:
        dict: A dictionary where each key is a document ID and the value is the document data.

    Raises:
        HTTPException: If an unexpected error occurs during retrieval (500).
    """
    try:
        return await words_service.get_by_difficulty(difficulty)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

#get by categories

@router.get("/texts/categories/{categories}")	
async def get_texts_categories_router(categories: str):
    """
    Retrieve text documents filtered by category.

    This endpoint fetches all text documents that contain the specified category 
    in their `categories` array.

    Args:
        categories (str): The category to filter text documents.

    Returns:
        dict: A dictionary where each key is a document ID and the value is the document data.

    Raises:
        HTTPException: If an unexpected error occurs during retrieval (500).
    """
    try:
        return await texts_service.get_by_categories(categories)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/words/categories/{categories}")
async def get_words_categories_router(categories: str):
    """
    Retrieve word documents filtered by category.

    This endpoint fetches all word documents that contain the specified category 
    in their `categories` array.

    Args:
        categories (str): The category to filter word documents.

    Returns:
        dict: A dictionary where each key is a document ID and the value is the document data.

    Raises:
        HTTPException: If an unexpected error occurs during retrieval (500).
    """
    try:
        return await words_service.get_by_categories(categories)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/sentences/categories/{categories}")	
async def get_sentences_categories_router(categories: str):
    """
    Retrieve sentence documents filtered by category.

    This endpoint fetches all sentence documents that contain the specified category 
    in their `categories` array.

    Args:
        categories (str): The category to filter sentence documents.

    Returns:
        dict: A dictionary where each key is a document ID and the value is the document data.

    Raises:
        HTTPException: If an unexpected error occurs during retrieval (500).
    """
    try:
        return await sentences_service.get_by_categories(categories)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

#delete by id

@router.delete("/texts/{document_id}")
async def delete_texts_id_router(document_id: str):
    """
    Delete a text document by its UID.

    This endpoint deletes a text document from the collection using the specified document ID.

    Args:
        document_id (str): The UID of the text document to delete.

    Returns:
        dict: A dictionary containing a confirmation message and the deleted document's ID.

    Raises:
        HTTPException: If an unexpected error occurs during deletion (500).
    """
    try:
        return await texts_service.delete_by_id(document_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.delete("/words/{document_id}")
async def delete_words_id_router(document_id: str):
    """
    Delete a word document by its UID.

    This endpoint deletes a word document from the collection using the specified document ID.

    Args:
        document_id (str): The UID of the word document to delete.

    Returns:
        dict: A dictionary containing a confirmation message and the deleted document's ID.

    Raises:
        HTTPException: If an unexpected error occurs during deletion (500).
    """
    try:
        return await words_service.delete_by_id(document_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.delete("/sentences/{document_id}")
async def delete_sentences_id_router(document_id: str):
    """
    Delete a sentence document by its UID.

    This endpoint deletes a sentence document from the collection using the specified document ID.

    Args:
        document_id (str): The UID of the sentence document to delete.

    Returns:
        dict: A dictionary containing a confirmation message and the deleted document's ID.

    Raises:
        HTTPException: If an unexpected error occurs during deletion (500).
    """
    try:
        return await sentences_service.delete_by_id(document_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

#post texts. words, sentences

@router.post("/sentences")
async def post_sentence_router(sentence: sentences):
    """
    Add a new sentence document to the collection.

    This endpoint creates a new sentence document using the provided data.

    Args:
        sentence (sentences): An instance of the `sentences` model containing the sentence data.

    Returns:
        dict: A dictionary containing a confirmation message and the UID of the new document.

    Raises:
        HTTPException: If an unexpected error occurs during document creation (500).
    """
    try:
        return await sentences_service.post_sentences(sentence)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.post("/texts")
async def post_texts_router(text: texts):
    """
    Add a new text document to the collection.

    This endpoint creates a new text document using the provided data.

    Args:
        text (texts): An instance of the `texts` model containing the text data.

    Returns:
        dict: A dictionary containing a confirmation message and the UID of the new document.

    Raises:
        HTTPException: If an unexpected error occurs during document creation (500).
    """
    try:
        return await texts_service.post_text(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.post("/words")
async def post_words_router(word: words):
    """
    Add a new word document to the collection.

    This endpoint creates a new word document using the provided data.

    Args:
        word (words): An instance of the `words` model containing the word data.

    Returns:
        dict: A dictionary containing a confirmation message and the UID of the new document.

    Raises:
        HTTPException: If an unexpected error occurs during document creation (500).
    """
    try:
        return await words_service.post_word(word)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

#post audio
@router.post("/sentences/audios")
async def post_sentences_audio_router(file: UploadFile = File(...)):
    """
    Upload an audio file for a sentence document.

    This endpoint uploads a `.flac` audio file associated with a sentence document. 
    The file is stored in cloud storage and the corresponding document is updated with its public URL.

    Args:
        file (UploadFile): The audio file to upload. Must be of type `.flac`.

    Returns:
        dict: A dictionary containing a confirmation message about the upload and URL update.

    Raises:
        HTTPException: If the file type is not supported or an unexpected error occurs during upload (500).
    """
    try:
        return await sentences_service.post_audio(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.post("/texts/audios")
async def post_texts_audio_router(file: UploadFile = File(...), chapter: str = Form(...)):
    """
    Upload an audio file for a text document.

    This endpoint uploads a `.flac` audio file associated with a text document. 
    The file is stored in cloud storage under the specified chapter folder, and the 
    corresponding document is updated with its public URL.

    Args:
        file (UploadFile): The audio file to upload. Must be of type `.flac`.
        chapter (str): The chapter ID to associate with the uploaded audio.

    Returns:
        dict: A dictionary containing a confirmation message about the upload and URL update.

    Raises:
        HTTPException: If the file type is not supported or an unexpected error occurs during upload (500).
    """
    try:
        return await texts_service.post_audio(file=file, chapter=chapter)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.post("/words/audios")
async def post_words_audio_router(file: UploadFile = File(...), text: str = Form(...)):
    """
    Upload an audio file for a word document.

    This endpoint uploads a `.flac` audio file associated with a word document. 
    The file is stored in cloud storage and the corresponding document is updated with its public URL.

    Args:
        file (UploadFile): The audio file to upload. Must be of type `.flac`.
        text (str): The text identifier to associate with the uploaded audio.

    Returns:
        dict: A dictionary containing a confirmation message about the upload and URL update.

    Raises:
        HTTPException: If the file type is not supported or an unexpected error occurs during upload (500).
    """
    try:
        return await words_service.post_audio(file= file, text= text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

#update evaluation
@router.put("/texts/evaluation")
async def update_texts_evaluation_router(texts_evaluation: TextsEvaluation):
    """
    Update the audio analysis evaluation of text documents.

    This endpoint updates the `audio_analysis` field for text documents 
    that match the chapter ID and audio file provided in `texts_evaluation`.

    Args:
        texts_evaluation (TextsEvaluation): An object containing the chapter ID, 
            audio file, and the audio analysis data to update.

    Returns:
        dict: A dictionary containing a confirmation message of the update.

    Raises:
        HTTPException: If no matching document is found or an unexpected error occurs (500).
    """
    try:
        return await texts_service.update_evaluation(texts_evaluation=texts_evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.put("/sentences/evaluation")
async def update_sentences_evaluation_router(sentences_evaluation: SentencesEvaluation):
    """
    Update the audio analysis evaluation of sentence documents.

    This endpoint updates the `audio_analysis` field for sentence documents 
    that match the chapter ID and audio file provided in `sentences_evaluation`.

    Args:
        sentences_evaluation (SentencesEvaluation): An object containing the chapter ID, 
            audio file, and the audio analysis data to update.

    Returns:
        dict: A dictionary containing a confirmation message of the update.

    Raises:
        HTTPException: If no matching document is found or an unexpected error occurs (500).
    """
    try:
        return await sentences_service.update_evaluation(sentences_evaluation=sentences_evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.put("/words/evaluation")
async def update_words_evaluation_router(words_evaluation: WordsEvaluation):
    """
    Update the audio analysis evaluation of word documents.

    This endpoint updates the `audio_analysis` field for word documents 
    that match the chapter ID and audio file provided in `words_evaluation`.

    Args:
        words_evaluation (WordsEvaluation): An object containing the chapter ID, 
            audio file, and the audio analysis data to update.

    Returns:
        dict: A dictionary containing a confirmation message of the update.

    Raises:
        HTTPException: If no matching document is found or an unexpected error occurs (500).
    """
    try:
        return await words_service.update_evaluation(words_evaluation=words_evaluation)    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

#update audio_duration
@router.put("/texts/audio_duration")
async def update_texts_audio_duration_router(texts_audio_duration: TextsAudioDuration):
    """
    Update the audio duration of text documents.

    This endpoint updates the `audio_duration` field for text documents 
    that match the chapter ID and audio file provided in `texts_audio_duration`.

    Args:
        texts_audio_duration (TextsAudioDuration): An object containing the chapter ID, 
            audio file, and the audio duration to update.

    Returns:
        dict: A dictionary containing a confirmation message of the update.

    Raises:
        HTTPException: If no matching document is found or an unexpected error occurs (500).
    """
    try:
        return await texts_service.update_audio_duration(texts_audio_duration=texts_audio_duration)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
@router.put("/sentences/audio_duration")
async def update_sentences_audio_duration_router(sentences_audio_duration: SentencesAudioDuration):
    """
    Update the audio duration of sentence documents.

    This endpoint updates the `audio_duration` field for sentence documents 
    that match the chapter ID and audio file provided in `sentences_audio_duration`.

    Args:
        sentences_audio_duration (SentencesAudioDuration): An object containing the chapter ID, 
            audio file, and the audio duration to update.

    Returns:
        dict: A dictionary containing a confirmation message of the update.

    Raises:
        HTTPException: If no matching document is found or an unexpected error occurs (500).
    """
    try:
        return await sentences_service.update_audio_duration(sentences_audio_duration=sentences_audio_duration)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
@router.put("/words/audio_duration")
async def update_words_audio_duration_router(words_audio_duration: WordsAudioDuration):
    """
    Update the audio duration of word documents.

    This endpoint updates the `audio_duration` field for word documents 
    that match the chapter ID and audio file provided in `words_audio_duration`.

    Args:
        words_audio_duration (WordsAudioDuration): An object containing the chapter ID, 
            audio file, and the audio duration to update.

    Returns:
        dict: A dictionary containing a confirmation message of the update.

    Raises:
        HTTPException: If no matching document is found or an unexpected error occurs (500).
    """
    try:
        return await words_service.update_audio_duration(words_audio_duration=words_audio_duration)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")