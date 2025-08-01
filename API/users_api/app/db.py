import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore, storage
from app.config import FIREBASE_CREDENTIALS


cred = credentials.Certificate(FIREBASE_CREDENTIALS)
firebase_admin.initialize_app(cred, {
        'storageBucket': 'echo-9f9e9.firebasestorage.app'
})

db = firestore.client()
bucket = storage.bucket()

