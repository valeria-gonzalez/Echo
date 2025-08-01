from app.db import db
#from app.schemas.resourses_schemas import sentences, texts, words, TextsEvaluation, SentencesEvaluation
from google.cloud.firestore_v1 import FieldFilter
from fastapi import HTTPException, UploadFile, Form
from firebase_admin import storage

class UserApplicationService:
    """Service for userapplication-related operations in the Firestore database."""
    
    def __init__(self):
        self.user_application_ref = db.collection("user_aplication")
        self.progress_ref = self.user_application_ref.collection("progress")

    