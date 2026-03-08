# backend/app/models/student.py
from pydantic import BaseModel
from typing import List, Optional

class Student(BaseModel):
    student_id: str
    lab_id: str
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    health_issues: Optional[List[str]] = []
    experiment_group: str

    # ✅ FIX: Default to "" — route sets the real value server-side
    timestamp: str = ""