# Resources API
The Resources API provides endpoints for managin 
**texts**, **sentences** and **words**

## Requirements ⚙️⚙️⚙️

```bash
pip install fastapi
pip install uvicorn
pip install firebase-admin
pip install python-multipart
pip install dotenv
```

Alternatively, can use the file requeriments.txt

```bash
pip install -r requeriments.txt
```

## `.env` File Setup

Create a file named `.env` in the root of your project and add the following line:

```env
FIREBASE_CREDENTIAL="hereyourkey.json"

## project structure 

```

└── resources                          # Project root folder (may contain docs and dependency files)
    ├── app
    │   ├── config.py                   # General app configuration (environment variables, constants, etc.)
    │   ├── db.py                       # Database connection and setup
    │   ├── main.py                     # Main entry point of the FastAPI application
    ├── readme.md                       # General project documentation
    ├── requirements.txt                # List of Python dependencies required for the project
    ├── routers                         # Folder containing API route handlers (controllers)
    │   ├── __init__.py                 # Marks the directory as a Python package
    │   └── resources_router.py         # Defines API endpoints related to "resources"
    ├── schemas                         # Pydantic models for data validation and structure
    │   ├── __init__.py                 # Marks the directory as a Python package
    │   └── resources_schemas.py        # Pydantic models specifically for "resources"
    ├── service                         # Business logic and functions that interact with the database
    │   ├── __init__.py                 # Marks the directory as a Python package
    │   ├── sentences_service.py        # Services and operations related to "sentences"
    │   ├── texts_service.py            # Services and operations related to "texts"
    │   └── words_service.py            # Services and operations related to "words"

```

## Running the API🚀🚀🚀

Run the following command in a directory that contains the `app` folder:

```bash
uvicorn app.main:app --reload --port 8001


```bash
you should see output similar to this
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [21359] using StatReload
INFO:     Started server process [21361]
```

to explore all avalible API endpoints and their functionalities, visit:
 http://127.0.0.1:8000

 ## API resources includes the following endpoints: 🧠

### 1. Get all texts
- **URL:** `http://127.0.0.1:8001/texts`
- **Method:** GET
- **Request:** No path or body parameters required
- **Response:** Returns a list of all text documents (you can describe the structure here)

---

### 2. Get all sentences
- **URL:** `http://127.0.0.1:8001/sentences`
- **Method:** GET
- **Request:** No path or body parameters required
- **Response:** Returns a list of all sentence documents (you can describe the structure here)

---

### 3. Get all words
- **URL:** `http://127.0.0.1:8001/words`
- **Method:** GET
- **Request:** No path or body parameters required
- **Response:** Returns a list of all word documents (you can describe the structure here)


### 4. Get a text by ID
- **URL:** `http://127.0.0.1:8001/texts/{id}`
- **Method:** GET
- **Request:** 
  - **Path parameter:** `id` (string) → UID of the text document to retrieve  
  - No body parameters required
- **Response:** Returns a dictionary representing the text document (you can describe the fields here)

---

### 5. Get a sentence by ID
- **URL:** `http://127.0.0.1:8001/sentences/{id}`
- **Method:** GET
- **Request:** 
  - **Path parameter:** `id` (string) → UID of the sentence document to retrieve  
  - No body parameters required
- **Response:** Returns a dictionary representing the sentence document (you can describe the fields here)

---

### 6. Get a word by ID
- **URL:** `http://127.0.0.1:8001/words/{id}`
- **Method:** GET
- **Request:** 
  - **Path parameter:** `id` (string) → UID of the word document to retrieve  
  - No body parameters required
- **Response:** Returns a dictionary representing the word document (you can describe the fields here)

### 7. Get texts by chapter ID
- **URL:** `http://127.0.0.1:8001/texts/chapter/{id}`
- **Method:** GET
- **Request:** 
  - **Path parameter:** `id` (string) → Chapter ID to filter text documents  
  - No body parameters required
- **Response:** Returns a dictionary where each key is a document ID and the value is the document data

---

### 8. Get sentences by audio ID
- **URL:** `http://127.0.0.1:8001/sentences/audio_id/{id}`
- **Method:** GET
- **Request:** 
  - **Path parameter:** `id` (integer) → Audio ID to filter sentence documents  
  - No body parameters required
- **Response:** Returns a dictionary where each key is a document ID and the value is the document data

---

### 9. Get words by text
- **URL:** `http://127.0.0.1:8001/words/text/{id}`
- **Method:** GET
- **Request:** 
  - **Path parameter:** `id` (string) → Text used to filter word documents  
  - No body parameters required
- **Response:** Returns a dictionary where each key is a document ID and the value is the document data


### 10. Get texts by difficulty
- **URL:** `http://127.0.0.1:8001/texts/difficulty/{difficulty}`
- **Method:** GET
- **Request:** 
  - **Path parameter:** `difficulty` (integer) → Difficulty level to filter text documents  
  - No body parameters required
- **Response:** Returns a dictionary where each key is a document ID and the value is the document data

---

### 11. Get sentences by difficulty
- **URL:** `http://127.0.0.1:8001/sentences/difficulty/{difficulty}`
- **Method:** GET
- **Request:** 
  - **Path parameter:** `difficulty` (integer) → Difficulty level to filter sentence documents  
  - No body parameters required
- **Response:** Returns a dictionary where each key is a document ID and the value is the document data

---

### 12. Get words by difficulty
- **URL:** `http://127.0.0.1:8001/words/difficulty/{difficulty}`
- **Method:** GET
- **Request:** 
  - **Path parameter:** `difficulty` (integer) → Difficulty level to filter word documents  
  - No body parameters required
- **Response:** Returns a dictionary where each key is a document ID and the value is the document data

### 13. Get texts by category
- **URL:** `http://127.0.0.1:8001/texts/categories/{categories}`
- **Method:** GET
- **Request:** 
  - **Path parameter:** `categories` (string) → Category to filter text documents  
  - No body parameters required
- **Response:** Returns a dictionary where each key is a document ID and the value is the document data

---

### 14. Get words by category
- **URL:** `http://127.0.0.1:8001/words/categories/{categories}`
- **Method:** GET
- **Request:** 
  - **Path parameter:** `categories` (string) → Category to filter word documents  
  - No body parameters required
- **Response:** Returns a dictionary where each key is a document ID and the value is the document data

---

### 15. Get sentences by category
- **URL:** `http://127.0.0.1:8001/sentences/categories/{categories}`
- **Method:** GET
- **Request:** 
  - **Path parameter:** `categories` (string) → Category to filter sentence documents  
  - No body parameters required
- **Response:** Returns a dictionary where each key is a document ID and the value is the document data


### 16. Delete a text by ID
- **URL:** `http://127.0.0.1:8001/texts/{document_id}`
- **Method:** DELETE
- **Request:** 
  - **Path parameter:** `document_id` (string) → UID of the text document to delete  
  - No body parameters required
- **Response:** Returns a dictionary containing a confirmation message and the deleted document's ID

---

### 17. Delete a word by ID
- **URL:** `http://127.0.0.1:8001/words/{document_id}`
- **Method:** DELETE
- **Request:** 
  - **Path parameter:** `document_id` (string) → UID of the word document to delete  
  - No body parameters required
- **Response:** Returns a dictionary containing a confirmation message and the deleted document's ID

---

### 18. Delete a sentence by ID
- **URL:** `http://127.0.0.1:8001/sentences/{document_id}`
- **Method:** DELETE
- **Request:** 
  - **Path parameter:** `document_id` (string) → UID of the sentence document to delete  
  - No body parameters required
- **Response:** Returns a dictionary containing a confirmation message and the deleted document's ID


### 19. Add a new sentence
- **URL:** `http://127.0.0.1:8001/sentences`
- **Method:** POST
- **Request:** 
  - **Body parameter:** JSON object representing a `sentence` (according to the `sentences` model)  
  - Example:
    ```json
        {
        "audio_url": "string",
        "text": "string",
        "difficulty": 0,
        "categories": [
            "string"
        ],
        "word_count": 0,
        "translation": "string",
        "audio_id": 0,
        "audio_analysis": {
            "number_of_syllables": 0,
            "number_of_pauses": 0,
            "speech_rate": 0,
            "articulation_rate": 0,
            "speaking_rate": 0,
            "speaking_duration": 0,
            "ratio": 0,
            "transcription": "string",
            "total_duration": 0
        }
        }
    ```
- **Response:** Returns a dictionary containing a confirmation message and the UID of the new sentence document

---

### 20. Add a new text
- **URL:** `http://127.0.0.1:8001/texts`
- **Method:** POST
- **Request:** 
  - **Body parameter:** JSON object representing a `text` (according to the `texts` model)  
  - Example:
    ```json
        {
        "audio_url": "string",
        "text": "string",
        "difficulty": 0,
        "categories": [
            "string"
        ],
        "word_count": 0,
        "book_title": "string",
        "translation": "string",
        "audio_analysis": {
            "number_of_syllables": 0,
            "number_of_pauses": 0,
            "speech_rate": 0,
            "articulation_rate": 0,
            "speaking_rate": 0,
            "speaking_duration": 0,
            "ratio": 0,
            "transcription": "string",
            "total_duration": 0
        },
        "chapter_id": "string",
        "audio_file": "string"
        }
    ```
- **Response:** Returns a dictionary containing a confirmation message and the UID of the new text document

---

### 21. Add a new word
- **URL:** `http://127.0.0.1:8001/words`
- **Method:** POST
- **Request:** 
  - **Body parameter:** JSON object representing a `word` (according to the `words` model)  
  - Example:
    ```json
        {
        "audio_url": "string",
        "text": "string",
        "difficulty": 0,
        "categories": [
            "string"
        ],
        "word_count": 0,
        "definitions": [
            {
            "pos": "string",
            "definitions": [
                "string"
            ]
            }
        ],
        "ipa": "string",
        "translation": [
            "string"
        ],
        "audio_analysis": {
            "number_of_syllables": 0,
            "number_of_pauses": 0,
            "speech_rate": 0,
            "articulation_rate": 0,
            "speaking_rate": 0,
            "speaking_duration": 0,
            "ratio": 0,
            "transcription": "string",
            "total_duration": 0
        }
        }
    ```
- **Response:** Returns a dictionary containing a confirmation message and the UID of the new word document


### 22. Upload an audio for a sentence
- **URL:** `http://127.0.0.1:8001/sentences/audios`
- **Method:** POST
- **Request:** 
  - **Form parameter:** `file` → Audio file of type `.mp3`  
  - No path parameters required
- **Response:** Returns a dictionary containing a confirmation message about the upload and URL update

---

### 23. Upload an audio for a text
- **URL:** `http://127.0.0.1:8001/texts/audios`
- **Method:** POST
- **Request:** 
  - **Form parameters:**  
    - `file` → Audio file of type `.flac`  
    - `chapter` → Chapter ID to associate with the uploaded audio  
  - No path parameters required
- **Response:** Returns a dictionary containing a confirmation message about the upload and URL update

---

### 24. Upload an audio for a word
- **URL:** `http://127.0.0.1:8001/words/audios`
- **Method:** POST
- **Request:** 
  - **Form parameters:**  
    - `file` → Audio file of type `.mp3`  
    - `text` → Text identifier to associate with the uploaded audio  
  - No path parameters required
- **Response:** Returns a dictionary containing a confirmation message about the upload and URL update

### 25. Update text evaluation
- **URL:** `http://127.0.0.1:8001/texts/evaluation`
- **Method:** PUT
- **Request:** 
  - **Body parameter:** JSON object representing a `TextsEvaluation`  
  - Example:
    ```json
        {
        "chapter_id": "string",
        "audio_file": "string",
        "audio_analysis": {
            "number_of_syllables": 0,
            "number_of_pauses": 0,
            "speech_rate": 0,
            "articulation_rate": 0,
            "speaking_rate": 0,
            "speaking_duration": 0,
            "ratio": 0,
            "transcription": "string",
            "total_duration": 0
        }
        }
    ```
- **Response:** Returns a dictionary containing a confirmation message of the update

---

### 26. Update sentence evaluation
- **URL:** `http://127.0.0.1:8001/sentences/evaluation`
- **Method:** PUT
- **Request:** 
  - **Body parameter:** JSON object representing a `SentencesEvaluation`  
  - Example:
    ```json
        {
        "audio_id": 0,
        "audio_analysis": {
            "number_of_syllables": 0,
            "number_of_pauses": 0,
            "speech_rate": 0,
            "articulation_rate": 0,
            "speaking_rate": 0,
            "speaking_duration": 0,
            "ratio": 0,
            "transcription": "string",
            "total_duration": 0
        }
        }
    ```
- **Response:** Returns a dictionary containing a confirmation message of the update

---

### 27. Update word evaluation
- **URL:** `http://127.0.0.1:8001/words/evaluation`
- **Method:** PUT
- **Request:** 
  - **Body parameter:** JSON object representing a `WordsEvaluation`  
  - Example:
    ```json
        {
        "text": "string",
        "audio_analysis": {
            "number_of_syllables": 0,
            "number_of_pauses": 0,
            "speech_rate": 0,
            "articulation_rate": 0,
            "speaking_rate": 0,
            "speaking_duration": 0,
            "ratio": 0,
            "transcription": "string",
            "total_duration": 0
        }
        }
    ```
- **Response:** Returns a dictionary containing a confirmation message of the update

### 28. Update text audio duration
- **URL:** `http://127.0.0.1:8001/texts/audio_duration`
- **Method:** PUT
- **Request:** 
  - **Body parameter:** JSON object representing a `TextsAudioDuration`  
  - Example:
    ```json
        {
        "chapter_id": "string",
        "audio_file": "string",
        "audio_duration": 0
        }
    ```
- **Response:** Returns a dictionary containing a confirmation message of the update

---

### 29. Update sentence audio duration
- **URL:** `http://127.0.0.1:8001/sentences/audio_duration`
- **Method:** PUT
- **Request:** 
  - **Body parameter:** JSON object representing a `SentencesAudioDuration`  
  - Example:
    ```json
        {
        "audio_id": 0,
        "audio_duration": 0
        }
    ```
- **Response:** Returns a dictionary containing a confirmation message of the update

---

### 30. Update word audio duration
- **URL:** `http://127.0.0.1:8001/words/audio_duration`
- **Method:** PUT
- **Request:** 
  - **Body parameter:** JSON object representing a `WordsAudioDuration`  
  - Example:
    ```json
        {
        "text": "string",
        "audio_duration": 0
        }
    ```
- **Response:** Returns a dictionary containing a confirmation message of the update
