# backend/app/models/session.py
from pydantic import BaseModel
from typing import List, Optional

class Session(BaseModel):
    session_id: str
    lab_id: str
    session_name: Optional[str] = None

    # Admin sets these in dd-mm-yyyy HH:MM:SS format
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    status: str = "active"

    devices: List[int] = []
    indoor_devices: List[int] = []
    outdoor_devices: List[int] = []

    occupancy: Optional[int] = None
    ac_status: Optional[str] = "OFF"
    ac_temperature: Optional[float] = None
    ac_mode: Optional[str] = None        # cooling / heating / fan / dry / auto
    windows: Optional[str] = "Closed"
    doors: Optional[str] = "Closed"
    ceiling_fan: Optional[str] = "Off"

    ventilation_strategy: Optional[str] = None
    created_by: Optional[str] = None

    timestamp: str = ""