from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add parent directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from routers.evaluation_router import router_evaluation
from routers.classifier_router import router_classification

app = FastAPI(title="Pronunciation Evaluation API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_evaluation)
app.include_router(router_classification)

@app.get("/")
async def root():
    return {"message": "Welcome to the Pronunciation Evaluation API!"}

if __name__ == "__main__":
    # If below doesn't work, run in terminal: uvicorn app.main:app --reload
    import uvicorn
    uvicorn.run(
        "app.main:app", 
        reload=True, 
        port=8000, 
        host="127.0.0.1", 
        reload_delay=0.1
    )
    
    