# backend/app/models/device.py
from pydantic import BaseModel
from typing import Optional

class Device(BaseModel):
    device_id: int                  # Unique device ID from API
    name: Optional[str] = None      # Friendly name
    type: str                       # "indoor" or "outdoor"
    location: Optional[str] = None  # Lab or area
    api_enabled: bool = True        # Whether to fetch from API

    # ✅ FIX: Default to "" — route sets the real value server-side
    timestamp: str = ""