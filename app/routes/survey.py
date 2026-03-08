# backend/app/routes/survey.py
from fastapi import APIRouter, HTTPException
from app.models.survey_response import SurveyResponse
from app.database import survey_responses_col
from app.utils.timestamp import current_timestamp

router = APIRouter(prefix="/survey", tags=["survey"])

@router.post("/submit")
def submit_survey(response: SurveyResponse):
    # ✅ FIX: Prevent duplicate survey submissions for same student + session
    existing = survey_responses_col.find_one({
        "student_id": response.student_id,
        "session_id": response.session_id
    })
    if existing:
        raise HTTPException(400, "Survey already submitted for this session")

    # Add timestamp
    response.timestamp = current_timestamp()

    # Save to MongoDB
    survey_responses_col.insert_one(response.dict())

    return {"status": "success", "message": "Survey submitted successfully"}

# ✅ NEW: Get all survey responses for a session (useful for admin dashboard)
@router.get("/session/{session_id}")
def get_session_responses(session_id: str):
    responses = list(survey_responses_col.find({"session_id": session_id}))
    for r in responses:
        r["_id"] = str(r["_id"])
    return responses