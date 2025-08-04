from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.resources_router import router 


app = FastAPI(title="Resources API",version = "1.0.0")

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Resourses API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
            "app.main:app", 
            host="0.0.0.0", 
            port=8000, 
            reload=True
            )
    
    