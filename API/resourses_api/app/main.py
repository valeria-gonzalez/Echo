from fastapi import FastAPI
from app.routers.resourses_router import router 



app = FastAPI(title="Resourses API",version = "1.0.0")

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Resourses API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    
    