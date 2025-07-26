# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access variables
ARLI_API_KEY = os.getenv("ARLI_API_KEY")
if ARLI_API_KEY is None:
    raise ValueError("ARLI_API_KEY not found in environment variables.")