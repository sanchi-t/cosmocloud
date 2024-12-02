from motor.motor_asyncio import AsyncIOMotorClient
import os

client = AsyncIOMotorClient("mongodb+srv://test-user:" + os.environ.get("MONGO_PASS") + "@cluster0.lxmxcq5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["student_management"]

