import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore, storage


cred = credentials.Certificate("/home/alan-ramos/Escritorio/echo/issue39sjson/echo-9f9e9-firebase-adminsdk-fbsvc-3550993856.json")
firebase_admin.initialize_app(cred, {
        'storageBucket': 'echo-9f9e9.firebasestorage.app'
})

db = firestore.client()
bucket = storage.bucket()

