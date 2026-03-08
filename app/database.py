# backend/app/database.py
from pymongo import MongoClient, ASCENDING
from app.config import MONGO_URI

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["lab_survey"]  # Database name

# Collections
students_col = db["students"]
devices_col = db["devices"]
sessions_col = db["sessions"]
survey_responses_col = db["survey_responses"]
admins_col = db["admins"]

# ✅ FIX: Add indexes for frequent queries and prevent duplicates
students_col.create_index(
    [("student_id", ASCENDING), ("lab_id", ASCENDING)],
    unique=True
)
sessions_col.create_index(
    [("lab_id", ASCENDING), ("status", ASCENDING)]
)
survey_responses_col.create_index(
    [("student_id", ASCENDING), ("session_id", ASCENDING)],
    unique=True
)
admins_col.create_index(
    [("email", ASCENDING)],
    unique=True
)