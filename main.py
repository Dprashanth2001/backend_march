from fastapi import FastAPI # type: ignore
from pydantic import BaseModel
from pymongo import MongoClient # type: ignore
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Load .env file
load_dotenv()

# MongoDB connection using environment variable
mongo_uri = os.getenv("MONGO_API_URI")

# MongoDB connection
client = MongoClient(mongo_uri)
db = client["mydb"]
collection = db["responses"]

app = FastAPI()

# Add this after creating FastAPI instance
origins = [
    "http://localhost:3000",  # React frontend
    "http://127.0.0.1:3000",  # sometimes needed
    "https://frontend-march.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # allow React frontend
    allow_credentials=True,
    allow_methods=["*"],      # allow GET, POST, etc.
    allow_headers=["*"],      # allow headers
)

# Define request model
class SurveyData(BaseModel):
    student_id: str
    q1: int
    q2: int
    q3: int
    q4: str

# Simple POST endpoint
@app.post("/submit")
def submit_survey(data: SurveyData):
    # Insert into MongoDB
    collection.insert_one(data.dict())
    return {"status": "success", "message": "Data saved!"}

# Test GET endpoint
@app.get("/")
def root():
    return {"message": "FastAPI backend is running"}