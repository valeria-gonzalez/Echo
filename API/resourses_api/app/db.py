import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('/home/alan-ramos/Escritorio/echo/issue39sjson/echo-9f9e9-firebase-adminsdk-fbsvc-3550993856.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()