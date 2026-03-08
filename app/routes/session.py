# backend/app/routes/session.py
from fastapi import APIRouter, HTTPException
from app.models.session import Session
from app.database import sessions_col
from app.utils.timestamp import current_timestamp

router = APIRouter(prefix="/session", tags=["session"])

@router.post("/create")
def create_session(session: Session):
    session.timestamp = current_timestamp()
    # Use admin-provided start_time if given, else set to now
    if not session.start_time:
        session.start_time = current_timestamp()

    if sessions_col.find_one({"session_id": session.session_id}):
        raise HTTPException(400, f"Session ID '{session.session_id}' already exists")

    sessions_col.insert_one(session.dict())
    return {"status": "success", "message": "Session created successfully"}

@router.get("/active/{lab_id}")
def get_active_session(lab_id: str):
    session = sessions_col.find_one({"lab_id": lab_id, "status": "active"})
    if not session:
        return {"status": "error", "message": "No active session for this lab"}
    session["_id"] = str(session["_id"])
    return session

@router.patch("/end/{session_id}")
def end_session(session_id: str):
    result = sessions_col.update_one(
        {"session_id": session_id, "status": "active"},
        {"$set": {"status": "completed", "end_time": current_timestamp()}}
    )
    if result.matched_count == 0:
        raise HTTPException(404, "Active session not found with this ID")
    return {"status": "success", "message": f"Session {session_id} marked as completed"}

@router.get("/list/{lab_id}")
def list_sessions(lab_id: str):
    sessions = list(sessions_col.find({"lab_id": lab_id}))
    for s in sessions:
        s["_id"] = str(s["_id"])
    return sessions