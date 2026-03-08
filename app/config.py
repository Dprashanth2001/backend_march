# backend/app/config.py
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_API_URI")  # MongoDB connection string
API_KEY = os.getenv("API_KEY")          # Optional: external device API key