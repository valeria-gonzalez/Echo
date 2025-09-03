# Users API
The Users API provides endpoints for managing **users**, **user applications**, **progress**, and **profile pictures**.

## Requirements ⚙️⚙️⚙️

```bash
pip install fastapi
pip install uvicorn
pip install firebase-admin
pip install python-multipart
pip install pydantic
pip install python-dotenv
```

Alternatively, you can use the requirements.txt file:
pip install -r requirements.txt


## `.env` File Setup

Create a file named `.env` in the root of your project and add the following line:

```env
FIREBASE_CREDENTIAL="hereyourkey.json"


## Project Structure
```env
├── app
│   ├── config.py
│   ├── db.py
│   ├── __init__.py
│   └── main.py
├── routers
│   ├── auth_router.py
│   └── users_router.py
├── schemas
│   └── users_schemas.py
├── service
│   ├── userApplication_service.py
│   └── users_service.py
├── utils
│   └── hash.py

## Running the API🚀🚀🚀

Run the following command in a directory that contains the `app` folder:

```bash
uvicorn app.main:app --reload --port 8000


```bash
you should see output similar to this
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [21359] using StatReload
INFO:     Started server process [21361]
```

to explore all avalible API endpoints and their functionalities, visit:
 http://127.0.0.1:8000

  ## API users includes the following endpoints: 🧠

### 1. Users API Root
- **URL:** `/users/`
- **Method:** GET
- **Request:** No path or body parameters required
- **Response:** Returns a welcome message indicating the API is running

**Example Response:**  
```json
{
  "message": "Welcome to the Users API!"
}

### 2. Get User by UID
- **URL:** `/users/account/{uid_user}`
- **Method:** GET
- **Request:** 
  - **Path Parameter:**  
    - `uid_user` (string) — The unique identifier of the user.
- **Response:** Returns the user's data including the Firestore document ID.
- **Errors:**
  - `404 Not Found` — If the user is not found.
  - `500 Internal Server Error` — If an unexpected error occurs while fetching the user.

**Example Response:**  
```json
{
  "id": "8PVzTlj1fHIOuk9S6ha8",
  "email": "readme",
  "name": "readme",
  "password": "$2b$12$q97No6G6HgfHEQYDvBvgXelFDWGR1Tp6U.u1KN8G1I/rPGFfc7IF6",
  "disables": true
}

### 3. Get User Application by UID
- **URL:** `/users/user_application/{uid_user}`
- **Method:** GET
- **Request:** 
  - **Path Parameter:**  
    - `uid_user` (string) — The unique identifier of the user.
- **Response:** Returns the user's application data including the Firestore document ID.
- **Errors:**
  - `404 Not Found` — If the user application is not found.
  - `500 Internal Server Error` — If an unexpected error occurs while fetching the data.

**Example Response:**  
```json
{
  "id": "u2CeJSI9TCCDByo9kcho",
  "profile_picture": "string",
  "gender": 0,
  "last_login": "2025-09-03T18:41:17.244000+00:00",
  "username": "readme",
  "creation_date": "2025-09-03T18:41:17.244000+00:00",
  "user_uid": "8PVzTlj1fHIOuk9S6ha8",
  "date_of_birth": "2025-09-03T18:41:17.244000+00:00"
}

### 4. Add New User
- **URL:** `/users/account`
- **Method:** POST
- **Request:** 
  - **Body Parameter:**  
    - `user` (object) — The user object containing user data.  
      **Example structure:**
      ```json
      {
        "uid": "123abc",
        "name": "John Doe",
        "email": "john@example.com",
        "other_field": "value"
      }
      ```
- **Response:** Returns a confirmation message with the Firestore document ID.
- **Errors:**
  - `500 Internal Server Error` — If an unexpected error occurs while adding the user.

**Example Response:**  
```json
{
  "message": "User added successfully",
  "document_id": "abc123"
}

### 5. Add New User Application
- **URL:** `/users/user_application`
- **Method:** POST
- **Request:** 
  - **Body Parameter:**  
    - `user_application` (object) — The user application object containing user data.  
      **Example structure:**
      ```json
        {
        "user_uid": "8PVzTlj1fHIOuk9S6ha8",
        "last_login": "2025-09-03T18:41:17.244Z",
        "creation_date": "2025-09-03T18:41:17.244Z",
        "date_of_birth": "2025-09-03T18:41:17.244Z",
        "gender": 0,
        "profile_picture": "string",
        "username": "readme"
        }
      ```
- **Response:** Returns a confirmation message with the Firestore document ID.
- **Errors:**
  - `500 Internal Server Error` — If an unexpected error occurs while adding the user application.

**Example Response:**  
```json
{
  "message": "User add",
  "doc_id": "u2CeJSI9TCCDByo9kcho"
}

### 6. Update User Application
- **URL:** `/users/user_application`
- **Method:** PUT
- **Request:** 
  - **Body Parameter:**  
    - `user_application` (object) — The user application object containing updated data.  
      **Example structure:**
      ```json
        {
        "user_uid": "8PVzTlj1fHIOuk9S6ha8",
        "last_login": "2025-09-03T18:45:37.985Z",
        "creation_date": "2025-09-03T18:45:37.985Z",
        "date_of_birth": "2025-09-03T18:45:37.985Z",
        "gender": 0,
        "profile_picture": "string",
        "username": "string"
        }
      ```
- **Response:** Returns a confirmation message with the Firestore document ID.
- **Errors:**
  - `404 Not Found` — If the user application is not found.
  - `500 Internal Server Error` — If an unexpected error occurs while updating the application.

**Example Response:**  
```json
{
  "message": "user_application update",
  "doc_id": "u2CeJSI9TCCDByo9kcho"
}

### 7. Add or Update User Application Progress
- **URL:** `/users/user_application/progress/{uid_user}`
- **Method:** POST
- **Request:** 
  - **Path Parameter:**  
    - `uid_user` (string) — The unique identifier of the user.
  - **Body Parameter:**  
    - `progress` (object) — The progress object containing resource progress data.  
      **Example structure:**
      ```json
        {
        "resource_uid": "string",
        "type": 0,
        "completed": true,
        "completion_date": "2025-09-03T18:47:15.647Z",
        "attempts": 0,
        "last_attempt": "2025-09-03T18:47:15.647Z",
        "evaluation": {
            "audio_url": "string",
            "total_score": 0,
            "clarity_score": 0,
            "speed_score": 0,
            "articulation_score": 0,
            "clarity_tip": "string",
            "speed_tip": "string",
            "rythm_tip": "string",
            "articulation_tip": "string"
        },
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
- **Response:** Returns a confirmation message with the Firestore document ID.
- **Errors:**
  - `404 Not Found` — If the user is not found.
  - `500 Internal Server Error` — If an unexpected error occurs while adding or updating progress.

**Example Response:**  
```json
{
  "message": "progress added",
  "doc_id": "209lwios99z2kAggWwq2"
}

### 8. Get User Progress with Attempts > 0
- **URL:** `/users/progress/attempts/{uid_user}`
- **Method:** GET
- **Request:** 
  - **Path Parameter:**  
    - `uid_user` (string) — The unique identifier of the user.
- **Response:** Returns a list of progress records with attempts greater than zero, each including the Firestore document ID and data.
- **Errors:**
  - `404 Not Found` — If no progress with attempts > 0 is found for the user.
  - `500 Internal Server Error` — If an unexpected error occurs during retrieval.

**Example Response:**  
```json
[
  {
    "id": "209lwios99z2kAggWwq2",
    "resource_uid": "string",
    "audio_analysis": {
      "number_of_syllables": 0,
      "speech_rate": 0,
      "number_of_pauses": 0,
      "total_duration": 0,
      "speaking_rate": 0,
      "speaking_duration": 0,
      "ratio": 0,
      "articulation_rate": 0,
      "transcription": "string"
    },
    "evaluation": {
      "rythm_tip": "string",
      "total_score": 0,
      "clarity_score": 0,
      "audio_url": "string",
      "clarity_tip": "string",
      "speed_score": 0,
      "articulation_score": 0,
      "speed_tip": "string",
      "articulation_tip": "string"
    },
    "completion_date": "2025-09-03T18:47:15.647000+00:00",
    "attempts": 10,
    "last_attempt": "2025-09-03T18:47:15.647000+00:00",
    "type": 0,
    "completed": true
  }
]

### 9. Get Completed User Progress
- **URL:** `/users/progress/completed/{uid_user}`
- **Method:** GET
- **Request:** 
  - **Path Parameter:**  
    - `uid_user` (string) — The unique identifier of the users.
- **Response:** Returns a list of completed progress records, each including the Firestore document ID and data.
- **Errors:**
  - `404 Not Found` — If no completed progress is found for the user.
  - `500 Internal Server Error` — If an unexpected error occurs during retrieval.

**Example Response:**  
```json
[
  {
    "id": "209lwios99z2kAggWwq2",
    "resource_uid": "string",
    "audio_analysis": {
      "number_of_syllables": 0,
      "speech_rate": 0,
      "number_of_pauses": 0,
      "total_duration": 0,
      "speaking_rate": 0,
      "speaking_duration": 0,
      "ratio": 0,
      "articulation_rate": 0,
      "transcription": "string"
    },
    "evaluation": {
      "rythm_tip": "string",
      "total_score": 0,
      "clarity_score": 0,
      "audio_url": "string",
      "clarity_tip": "string",
      "speed_score": 0,
      "articulation_score": 0,
      "speed_tip": "string",
      "articulation_tip": "string"
    },
    "completion_date": "2025-09-03T18:47:15.647000+00:00",
    "attempts": 10,
    "last_attempt": "2025-09-03T18:47:15.647000+00:00",
    "type": 0,
    "completed": true
  },
  {
    "id": "POcrvALmAwDs2Zl5h3to",
    "resource_uid": "st2ring",
    "audio_analysis": {
      "number_of_syllables": 0,
      "speech_rate": 0,
      "number_of_pauses": 0,
      "total_duration": 0,
      "speaking_rate": 0,
      "speaking_duration": 0,
      "ratio": 0,
      "articulation_rate": 0,
      "transcription": "string"
    },
    "evaluation": {
      "rythm_tip": "string",
      "total_score": 0,
      "clarity_score": 0,
      "audio_url": "string",
      "clarity_tip": "string",
      "speed_score": 0,
      "articulation_score": 0,
      "speed_tip": "string",
      "articulation_tip": "string"
    },
    "completion_date": "2025-09-03T18:47:15.647000+00:00",
    "attempts": 10,
    "last_attempt": "2025-09-03T18:47:15.647000+00:00",
    "type": 0,
    "completed": true
  }
]

### 10. Get User Progress by Resource
- **URL:** `/users/progress/{uid_user_application}/{uid_resource}`
- **Method:** GET
- **Request:** 
  - **Path Parameters:**  
    - `uid_user_application` (string) — The unique identifier of the user's application.  
    - `uid_resource` (string) — The unique identifier of the resource.
- **Response:** Returns a list of progress records for the specified resource, each including the Firestore document ID and data.
- **Errors:**
  - `404 Not Found` — If no progress is found for the resource.
  - `500 Internal Server Error` — If an unexpected error occurs during retrieval.

**Example Response:**  
```json
[
  {
    "id": "209lwios99z2kAggWwq2",
    "last_attempt": "2025-09-03T18:47:15.647000+00:00",
    "type": 0,
    "completion_date": "2025-09-03T18:47:15.647000+00:00",
    "evaluation": {
      "audio_url": "string",
      "speed_score": 0,
      "clarity_score": 0,
      "articulation_tip": "string",
      "clarity_tip": "string",
      "speed_tip": "string",
      "rythm_tip": "string",
      "total_score": 0,
      "articulation_score": 0
    },
    "resource_uid": "string",
    "completed": true,
    "attempts": 10,
    "audio_analysis": {
      "speaking_duration": 0,
      "transcription": "string",
      "speech_rate": 0,
      "ratio": 0,
      "speaking_rate": 0,
      "articulation_rate": 0,
      "number_of_pauses": 0,
      "total_duration": 0,
      "number_of_syllables": 0
    }
  }
]

### 11. Upload User Profile Picture
- **URL:** `/users/user_application/profile_picture/{user_uid}`
- **Method:** POST
- **Request:** 
  - **Path Parameter:**  
    - `user_uid` (string) — The unique identifier of the user.
  - **Body Parameter:**  
    - `file` (UploadFile) — The image file to upload (PNG, JPEG, JPG, or WEBP).
- **Response:** Returns a confirmation message if the upload and URL update succeed.
- **Errors:**
  - `500 Internal Server Error` — If an error occurs during upload or URL update.

**Example Response:**  
```json
{
  "message": "Image and url update",
  "image_url": "https://storage.googleapis.com/echo-9f9e9.firebasestorage.app/profile_picture/modulo.jpg"
}

### 12. User Login
- **URL:** `/auth/login`
- **Method:** POST
- **Request:** 
  - **Body Parameter:**  
    - `data` (object) — The login data containing the user's email and password.  
      **Example structure:**
      ```json
      {
        "email": "john@example.com",
        "password": "your_password"
      }
      ```
- **Response:** Returns a confirmation message and the user ID if authentication succeeds.
- **Errors:**
  - `401 Unauthorized` — If the email or password is incorrect.
  - `500 Internal Server Error` — If an unexpected error occurs during login.

**Example Response:**  
```json
{
  "message": "login successful"
}
