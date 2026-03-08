# backend/app/models/admin.py
from pydantic import BaseModel
from typing import List, Optional

class Admin(BaseModel):
    admin_id: str
    name: str
    email: str
    hashed_password: str
    labs_managed: Optional[List[str]] = []

    # ✅ FIX: Default to "" — route sets the real value server-side
    timestamp: str = ""