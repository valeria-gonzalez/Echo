import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1 import FieldFilter

cred = credentials.Certificate('')
app = firebase_admin.initialize_app(cred)
db = firestore.client()
