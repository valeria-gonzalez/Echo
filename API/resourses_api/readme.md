# Resources API
The Resources API provides endpoints for managin 
**texts**, **sentences** and **words**

API resources includes the following endpoints: 🧠

*This endpoint returns all resources in a JSON object.*
Method GET | /texts
Method GET | /sentences
Method GET | /words

*The endpoints returns a JSON response with the data associated with the specified ID.*
Method GET | /texts/{id}
Method GET | /sentences/{id}
Method GET | /words/{id}

*The endpoints returns a List of JSON response with the data associated with the specified dificulty.*
Method GET | /texts/difficulty/{difficulty}
Method GET | /sentences/difficulty/{difficulty}
Method GET | /words/difficulty/{difficulty}

*The endpoints returns a List of JSON response with the data associated with the specified categorie.*
Method GET | /texts/categories/{categories}
Method GET | /words/categories/{categories}
Method GET | /sentences/categories/{categories}

*The endpoints removes the collection corresponding to the specified ID*
Method DELETE | /texts/{document_id}
Method DELETE | /sentences/{document_id}
Method DELETE | /words/{document_id}

*The following endpoints inserts a collection using the provided data*
Method POST | /sentences
Method POST | /texts
Method POST | /words

## Requirements ⚙️⚙️⚙️

```bash
pip install fastapi
pip install uvicorn
pip install firebase-admin
```

Alternatively, can use the file requeriments.txt

```bash
pip install -r requeriments.txt
```

## project structure 

```
└── resourses_api
    ├── app
    │   ├── db.py
    │   ├── main.py
    │   ├── routers
    │   │   ├── __init__.py
    │   │   └── resourses_router.py
    │   ├── schemas
    │   │   ├── __init__.py
    │   │   └── resourses_schemas.py
    │   └── service
    │       ├── __init__.py
    │       └── resourses_service.py
```

The resourses_api directory serves as the root for our API, the app folder contain all the funcionalities.

here directories within app:
routers: 
    This is where you.ll find the API endpoint(routes)

schemas:
    Contains the data structures for our resourses

service:
    Manage our resources and accting as an intermediary between the routers and the database

db.py:
    contain the conexion to the database

main.py:
    The primary file thatt initializes and run

To use the API, Follow these two steps:
1 - Obtain your Firebase JSON credentials and place this JSON file in a secure and accesible location

2 - open app /db.py, locate the line cred = credentials.certificate and replace the path


db.py file should look similar to this example


```
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('path/to/your/serviceAccountKey.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()
```

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

