# Resources API
The Resources API provides endpoints for managin 
**texts**, **sentences** and **words**

API resources includes the following endpoints: 🧠

*This endpoint returns all resources in a JSON object.*
@router.get("/texts")
@router.get("/sentences")
@router.get("/words")

*The endpoints returns a JSON response with the data associated with the specified ID.*
@router.get("/texts/{id}")
@router.get("/sentences/{id}")
@router.get("/words/{id}")	

*The endpoints returns a JSON response with the data associated with the specified Id_chapter to texts, audio_id to sentneces, text to words*
@router.get("/texts/chapter/{id}")
@router.get("/sentences/audio_id/{id}")
@router.get("/words/text/{id}")	

*The endpoints returns a List of JSON response with the data associated with the specified dificulty.*
@router.get("/texts/difficulty/{difficulty}")
@router.get("/sentences/difficulty/{difficulty}")
@router.get("/words/difficulty/{difficulty}")
@router.get("/texts/categories/{categories}")	
@router.get("/words/categories/{categories}")
@router.get("/sentences/categories/{categories}")

*The endpoints removes the collection corresponding to the specified ID*
@router.delete("/texts/{document_id}")
@router.delete("/words/{document_id}")
@router.delete("/sentences/{document_id}")

*The following endpoints inserts a collection using the provided data*
@router.post("/sentences")
@router.post("/texts")
@router.post("/words")

*The following endpoints inserts a audio using the provided data*
@router.post("/sentences/audios")
@router.post("/texts/audios")
@router.post("/words/audios")

*The following endpoints update a collection using the provided data*
@router.put("/texts/evaluation")
@router.put("/sentences/evaluation")
@router.put("/words/evaluation")

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

The resourses_api directory serves as the root for our API, the app folder contain all the funcionalities.

here directories within app:
routers: 
- This is where you.ll find the API endpoint(routes)

schemas:
- Contains the data structures for our resourses

service:
- Manage our resources and accting as an intermediary between the routers and the database

db.py:
- contain the conexion to the database

main.py:
- The primary file thatt initializes and run


## Running the API🚀🚀🚀

to start navigate to the resourses_api directory in your terminal and execute the following command:

```bash
uvicorn app.main:app --reload
```

```bash
you should see output similar to this
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [21359] using StatReload
INFO:     Started server process [21361]
```

to explore all avalible API endpoints and their functionalities, visit:
 http://127.0.0.1:8000

