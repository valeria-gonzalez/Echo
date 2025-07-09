from app.db import db
from schemas.resourses_schemas import sentences, texts, words

#obtiene uno pasando nombre de colection y id
async def get_one(collection_name: str,id_object: int):
    ref = db.collection(collection_name).document(id_object)
    docs = ref.get()
    if not docs.exists:
        raise HTTPException(status_code=404, detail= "file not found")
        
    return docs.to_dict()

#obtiene uno texto pasando id
async def get_one_text(id_object: int):
    ref = db.collection("texts").document(id_object)
    docs = ref.get()
    if not docs.exists:
        raise HTTPException(status_code=404, detail= "file not found")
        
    return docs.to_dict()

#obtiene uno sentences pasando id
async def get_one_sentences(id_object: int):
    ref = db.collection("sentences").document(id_object)
    docs = ref.get()
    if not docs.exists:
        raise HTTPException(status_code=404, detail= "file not found")
        
    return docs.to_dict()

#obtiene uno words pasando id
async def get_one_words(id_object: int):
    ref = db.collection("words").document(id_object)
    docs = ref.get()
    if not docs.exists:
        raise HTTPException(status_code=404, detail= "file not found")
        
    return docs.to_dict()

#obtiene un texto pasando la dificultad
#GET texts_difficulty_list {difficulty}: Returns a list of text information that have a specific difficulty.

async def get_sentences_difficulty(difficulty: int):
    docs = (db.collection("sentences").where(filter=FieldFilter("difficulty", "==", difficulty)).get())
    data = {doc.id: doc.to_dict() for doc in docs}
    return data

#obtiene un texto pasando la dificultad
#GET sentences_difficulty_list {difficulty}: Returns a list of sentence information that have a specific difficulty.

async def get_texts_difficulty(difficulty: int):
    docs = (db.collection("texts").where(filter=FieldFilter("difficulty", "==", difficulty)).get())
    data = {doc.id: doc.to_dict() for doc in docs}
    return data

#obtiene un texto pasando la dificultad
#GET words_difficulty_list {difficulty}: Returns a list of word information that have a specific difficulty.

async def get_words_difficulty(difficulty: int):
    docs = (db.collection("words").where(filter=FieldFilter("difficulty", "==", difficulty)).get())
    data = {doc.id: doc.to_dict() for doc in docs}
    return data

#GET text_category_list {category}: Returns a list of texts information that have a specific category.

async def get_texts_difficulty(categories: str):
    docs = (db.collection("texts").where(filter=FieldFilter("categories", "array_contains", categories)).get())
    data = {doc.id: doc.to_dict() for doc in docs}
    return data

#GET sentence_category_list {category}: Returns a list of sentence information that have a specific category.
async def get_sentences_difficulty(categories: str):
    docs = (db.collection("sentences").where(filter=FieldFilter("categories", "array_contains", categories)).get())
    data = {doc.id: doc.to_dict() for doc in docs}
    return data

#GET word_category_list {category}: Returns a list of word information that have a specific category.
async def get_words_difficulty(categories: str):
    docs = (db.collection("words").where(filter=FieldFilter("categories", "array_contains", categories)).get())
    data = {doc.id: doc.to_dict() for doc in docs}
    return data

#delete
async def delete_texts_id(document_id: str):
    db.collection("texts").document(document_id).delete()
    return {"message": "document delete", "id": document_id}

#delete
async def delete_words_id(document_id: str):
    db.collection("words").document(document_id).delete()
    return {"message": "document delete", "id": document_id}

#delete
async def delete_sentences_id(document_id: str):
    db.collection("sentences").document(document_id).delete()
    return {"message": "document delete", "id": document_id}








#POST ENDPOINTS

async def post_texts(text: texts):
    user_ref = db.collection("texts").document(text.id)
    user_ref.set(text.model_dump())
    return {"message": "text insert", "id": text.id}

async def post_words(word: words):
    user_ref = db.collection("words").document(word.id)
    user_ref.set(word.model_dump())
    return {"message": "word insert", "id": word.id}

async def post_sentences(sentence: sentences):
    user_ref = db.collection("sentences").document(str(sentence.id))
    user_ref.set(sentence.model_dump())
    return {"message": "sentence insert", "id": sentence.id}


async def get_sentences():
    ref = db.collection("sentences")
    docs = ref.stream()
    allcoletion = []

    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        allcoletion.append(data)
    
    return allcoletion


async def get_texts():
    ref = db.collection("texts")
    docs = ref.stream()
    allcoletion = []

    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        allcoletion.append(data)
    
    return allcoletion

async def get_words():
    ref = db.collection("words")
    docs = ref.stream()
    allcoletion = []

    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        allcoletion.append(data)
    
    return allcoletion