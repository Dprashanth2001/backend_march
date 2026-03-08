# backend/app/routes/auth.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.models.student import Student
from app.database import students_col, sessions_col
from app.utils.hash_group import assign_experiment_group
from app.utils.timestamp import current_timestamp

router = APIRouter(prefix="/auth", tags=["auth"])

# Request model
class LoginRequest(BaseModel):
    student_id: str
    lab_id: str

# Optional registration info
class StudentExtraInfo(BaseModel):
    student_id: str
    lab_id: str
    name: str
    age: int
    gender: str
    health_issues: List[str] = []

# --- LOGIN / REGISTER ---
@router.post("/login")
def student_login(req: LoginRequest):
    # ✅ FIX: Was using "is_active": True — now consistent with Session model's "status": "active"
    session = sessions_col.find_one({"lab_id": req.lab_id, "status": "active"})
    if not session:
        raise HTTPException(400, "No active session for this lab")

    session_id = session["session_id"]

    # Check if student already exists for this lab
    student = students_col.find_one({"student_id": req.student_id, "lab_id": req.lab_id})
    if student:
        student["_id"] = str(student["_id"])
        needs_extra_info = not student.get("name")
        return {
            "exists": True,
            "student": student,
            "session_id": session_id,
            "needs_extra_info": needs_extra_info
        }

    # Student not found → frontend shows full registration
    return {
        "exists": False,
        "session_id": session_id
    }

# --- REGISTER / FILL EXTRA INFO ---
@router.post("/register")
def register_student(extra_info: StudentExtraInfo):
    # ✅ Consistent: using "status": "active"
    session = sessions_col.find_one({
        "lab_id": extra_info.lab_id,
        "status": "active"
    })

    if not session:
        raise HTTPException(400, "No active session for this lab")

    session_id = session["session_id"]

    # Prevent duplicates
    existing_student = students_col.find_one({
        "student_id": extra_info.student_id,
        "lab_id": extra_info.lab_id
    })

    if existing_student:
        return {
            "status": "exists",
            "student_id": existing_student["student_id"],
            "experiment_group": existing_student["experiment_group"],
            "session_id": session_id
        }

    # Assign experiment group
    group = assign_experiment_group(extra_info.student_id, session_id)

    new_student = Student(
        student_id=extra_info.student_id,
        lab_id=extra_info.lab_id,
        name=extra_info.name,
        age=extra_info.age,
        gender=extra_info.gender,
        health_issues=extra_info.health_issues,
        experiment_group=group,
        timestamp=current_timestamp()
    )

    students_col.insert_one(new_student.dict())

    return {
        "status": "success",
        "student": new_student.dict(),
        "session_id": session_id
    }