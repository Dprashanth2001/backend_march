# # backend/app/routes/survey.py
# from fastapi import APIRouter, HTTPException
# from app.models.survey_response import SurveyResponse
# from app.database import survey_responses_col
# from app.utils.timestamp import current_timestamp

# router = APIRouter(prefix="/survey", tags=["survey"])

# @router.post("/submit")
# def submit_survey(response: SurveyResponse):
#     # ✅ FIX: Prevent duplicate survey submissions for same student + session
#     existing = survey_responses_col.find_one({
#         "student_id": response.student_id,
#         "session_id": response.session_id
#     })
#     if existing:
#         raise HTTPException(400, "Survey already submitted for this session")

#     # Add timestamp
#     response.timestamp = current_timestamp()

#     # Save to MongoDB
#     survey_responses_col.insert_one(response.dict())

#     return {"status": "success", "message": "Survey submitted successfully"}

# # ✅ NEW: Get all survey responses for a session (useful for admin dashboard)
# @router.get("/session/{session_id}")
# def get_session_responses(session_id: str):
#     responses = list(survey_responses_col.find({"session_id": session_id}))
#     for r in responses:
#         r["_id"] = str(r["_id"])
#     return responses

# backend/app/routes/survey.py
from fastapi import APIRouter, HTTPException
from app.models.survey_response import SurveyResponse
from app.database import survey_responses_col, sessions_col
from app.utils.timestamp import current_timestamp
from bson import ObjectId

router = APIRouter(prefix="/survey", tags=["survey"])

@router.post("/submit")
def submit_survey(response: SurveyResponse):
    # Resolve session_instance_id from the active session if not provided
    # This links the response to the exact session run, not just the session_id
    if not response.session_instance_id:
        active = sessions_col.find_one({
            "session_id": response.session_id,
            "status": "active"
        })
        if active:
            response.session_instance_id = str(active["_id"])

    # Prevent duplicate: same student + same session instance
    existing = survey_responses_col.find_one({
        "student_id": response.student_id,
        "session_instance_id": response.session_instance_id or response.session_id
    })
    if existing:
        raise HTTPException(400, "Survey already submitted for this session")

    response.timestamp = current_timestamp()
    survey_responses_col.insert_one(response.dict())
    return {"status": "success", "message": "Survey submitted successfully"}


@router.get("/session/{session_instance_id}")
def get_session_responses(session_instance_id: str):
    # Query by session_instance_id (MongoDB _id of session doc) — not session_id
    # This ensures morning and afternoon runs of the same session are counted separately
    responses = list(survey_responses_col.find({
        "session_instance_id": session_instance_id
    }))
    for r in responses:
        r["_id"] = str(r["_id"])
    return responses