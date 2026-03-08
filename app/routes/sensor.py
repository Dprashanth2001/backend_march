# backend/app/routes/sensor.py
import os
import httpx
from fastapi import APIRouter, HTTPException
from app.config import SENSOR_API_KEY, SENSOR_API_URL

router = APIRouter(prefix="/sensor", tags=["sensor"])


@router.get("/latest")
async def get_latest():
    """
    Proxy endpoint — frontend calls this over HTTPS,
    backend forwards to the sensor API over HTTP internally.
    Browser never sees the insecure request.
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            res = await client.post(
                SENSOR_API_URL,
                json={"apiKey": SENSOR_API_KEY},
                headers={"Content-Type": "application/json"},
            )
            res.raise_for_status()
            return res.json()
    except httpx.TimeoutException:
        raise HTTPException(504, "Sensor API timed out")
    except Exception as e:
        raise HTTPException(502, f"Sensor API error: {str(e)}")