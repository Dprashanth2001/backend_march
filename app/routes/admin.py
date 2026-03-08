# backend/app/routes/admin.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import hashlib
from app.models.admin import Admin
from app.database import admins_col
from app.utils.timestamp import current_timestamp

router = APIRouter(prefix="/admin", tags=["admin"])

# ✅ FIX: Separate request model so raw password is hashed before storing
class AdminCreateRequest(BaseModel):
    admin_id: str
    name: str
    email: str
    password: str  # plain text → will be hashed before saving
    labs_managed: Optional[List[str]] = []

class AdminLoginRequest(BaseModel):
    email: str
    password: str

def hash_password(password: str) -> str:
    """Simple SHA-256 hash. Use bcrypt in production."""
    return hashlib.sha256(password.encode()).hexdigest()

# ✅ FIX: Hash password before storing admin
@router.post("/add")
def add_admin(req: AdminCreateRequest):
    # Check duplicate email
    if admins_col.find_one({"email": req.email}):
        raise HTTPException(400, "Admin with this email already exists")

    admin = Admin(
        admin_id=req.admin_id,
        name=req.name,
        email=req.email,
        hashed_password=hash_password(req.password),
        labs_managed=req.labs_managed,
        timestamp=current_timestamp()
    )
    admins_col.insert_one(admin.dict())
    return {"status": "success", "message": "Admin added"}

# ✅ NEW: Admin login endpoint
@router.post("/login")
def admin_login(req: AdminLoginRequest):
    admin = admins_col.find_one({"email": req.email})
    if not admin:
        raise HTTPException(401, "Invalid email or password")

    if admin["hashed_password"] != hash_password(req.password):
        raise HTTPException(401, "Invalid email or password")

    return {
        "status": "success",
        "admin_id": admin["admin_id"],
        "name": admin["name"],
        "labs_managed": admin.get("labs_managed", [])
    }

@router.get("/list")
def list_admins():
    admins = list(admins_col.find())
    for d in admins:
        d["_id"] = str(d["_id"])
        d.pop("hashed_password", None)  # ✅ Never expose password hash in responses
    return admins