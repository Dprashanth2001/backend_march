# backend/app/routes/device.py
from fastapi import APIRouter, HTTPException
from app.models.device import Device
from app.database import devices_col
from app.utils.timestamp import current_timestamp

router = APIRouter(prefix="/device", tags=["device"])

@router.post("/add")
def add_device(device: Device):
    device.timestamp = current_timestamp()
    devices_col.insert_one(device.dict())
    return {"status": "success", "message": "Device added"}

# List all devices
@router.get("/list")
def list_devices():
    devices = list(devices_col.find())
    for d in devices:
        d["_id"] = str(d["_id"])
    return devices

# ✅ NEW: Get a single device by its device_id
@router.get("/{device_id}")
def get_device(device_id: int):
    device = devices_col.find_one({"device_id": device_id})
    if not device:
        raise HTTPException(404, f"Device {device_id} not found")
    device["_id"] = str(device["_id"])
    return device

# ✅ NEW: Delete a device by device_id
@router.delete("/{device_id}")
def delete_device(device_id: int):
    result = devices_col.delete_one({"device_id": device_id})
    if result.deleted_count == 0:
        raise HTTPException(404, f"Device {device_id} not found")
    return {"status": "success", "message": f"Device {device_id} deleted"}