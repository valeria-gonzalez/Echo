from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.users_router import router as users_router
from routers.auth_router import router as auth_router
app = FastAPI(title="Users API",version = "1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(auth_router)
@app.get("/")
async def root():
    return {"message": "Welcome to the Resourses API!"}

if __name__ == "__main__":
    # If below doesn't work, run in terminal: uvicorn app.main:app --reload
    import uvicorn
    uvicorn.run(
            "app.main:app", 
            host="0.0.0.0", 
            port=8003, 
            reload=True
            )
    
    