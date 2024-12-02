from typing import Optional
from fastapi import APIRouter, HTTPException, Path, Query
from app.db import db
from app.models import Student
from bson import ObjectId

router = APIRouter(prefix="/students")

@router.post("/", status_code=201)
async def create_student(student: Student):
    student_dict = student.dict()
    result = await db.students.insert_one(student_dict)
    return {"id": str(result.inserted_id)}

@router.get("/")
async def list_students(country: Optional[str] = Query(None), age: Optional[int] = Query(None)):
    query = {}
    if country:
        query["address.country"] = {"$regex": f"^{country}$", "$options": "i"}
    if age is not None:
        query["age"] = {"$gte": age}
    students = await db.students.find(query).to_list(100)
    return {"data": [{"name": s["name"], "age": s["age"]} for s in students]}

@router.get("/{id}")
async def fetch_student(id: str = Path(...)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid student ID format")
    
    student = await db.students.find_one({"_id": ObjectId(id)})
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student["id"] = str(student.pop("_id"))
    return {
        "name": student["name"],
        "age": student["age"],
        "address": student["address"]
    }

@router.patch("/{id}")
async def update_student(id: str, student: Student):
    update_data = {k: v for k, v in student.dict().items() if v is not None}
    result = await db.students.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    return {}

@router.delete("/{id}", status_code=200)
async def delete_student(id: str):
    result = await db.students.delete_one({"_id": ObjectId(id)})
    return {}

