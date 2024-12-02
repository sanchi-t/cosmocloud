from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Backend Intern Hiring Task", version="1.0.0")

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Student Management System"}

