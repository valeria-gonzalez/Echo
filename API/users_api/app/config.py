# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access variables
FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIAL")
if FIREBASE_CREDENTIALS is None:
    raise ValueError("FIREBASE_CREDENTIAL not found in environment variables.")