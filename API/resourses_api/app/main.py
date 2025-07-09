from fastapi import FastAPI
from fastapi import HTTPException
from routers.resourses_router import router
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1 import FieldFilter
from pydantic import BaseModel
from datetime import datetime
from typing import List


app = FastAPI(title="Resourses API",version = "1.0.0")

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Resourses API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    
    