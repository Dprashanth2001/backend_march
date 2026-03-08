# backend/app/utils/timestamp.py
from datetime import datetime

def current_timestamp():
    """
    Returns current timestamp in dd-mm-yyyy HH:MM:SS format
    """
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")