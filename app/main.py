# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import all routers
from app.routes import auth, survey, session, device, admin

app = FastAPI(title="Lab Survey Backend")

# CORS settings (React frontend URLs)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://frontend-march.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(survey.router)
app.include_router(session.router)
app.include_router(device.router)
app.include_router(admin.router)

# Health check endpoint
@app.get("/")
def root():
    return {"status": "success", "message": "FastAPI backend running"}