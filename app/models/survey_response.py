# # backend/app/models/survey_response.py
# from pydantic import BaseModel
# from typing import Optional, Dict

# class SurveyResponse(BaseModel):
#     student_id: str
#     session_id: str
#     experiment_group: str

#     # Survey answers
#     q1_air_freshness: Optional[int] = None
#     q2_thermal_comfort: Optional[int] = None
#     q3_alertness: Optional[int] = None
#     q3_concentration: Optional[int] = None
#     q4_need_ventilation: Optional[str] = None
#     q5_ventilation_preference: Optional[str] = None

#     # Sensor snapshots at time of survey (only populated for control group)
#     device_data: Optional[Dict] = {}
#     outdoor_device_data: Optional[Dict] = {}

#     timestamp: str = ""


# backend/app/models/survey_response.py
from pydantic import BaseModel
from typing import Optional, Dict

class SurveyResponse(BaseModel):
    student_id: str
    session_id: str
    # ✅ Unique identifier for each session run — MongoDB _id of the session document
    # Allows the same session_id (e.g. "SW1") to be reused across morning/afternoon
    session_instance_id: Optional[str] = None
    experiment_group: str

    q1_air_freshness: Optional[int] = None
    q2_thermal_comfort: Optional[int] = None
    q3_alertness: Optional[int] = None
    q3_concentration: Optional[int] = None
    q4_need_ventilation: Optional[str] = None
    q5_ventilation_preference: Optional[str] = None

    device_data: Optional[Dict] = {}
    outdoor_device_data: Optional[Dict] = {}

    timestamp: str = ""