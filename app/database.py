# backend/app/database.py
from pymongo import MongoClient, ASCENDING
from app.config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["lab_survey"]

# Collections
students_col         = db["students"]
devices_col          = db["devices"]
sessions_col         = db["sessions"]
survey_responses_col = db["survey_responses"]
admins_col           = db["admins"]

# ── Drop the old unique index that blocks session_id reuse ───────────────────
# The old index (student_id + session_id) prevented a student from submitting
# again when the same session_id is reused on a different day.
# We now use session_instance_id (MongoDB _id) to differentiate runs.
try:
    survey_responses_col.drop_index("student_id_1_session_id_1")
except Exception:
    pass  # index may not exist, that's fine

# ── Indexes ──────────────────────────────────────────────────────────────────
# Students: one registration per student per lab (still unique)
students_col.create_index(
    [("student_id", ASCENDING), ("lab_id", ASCENDING)],
    unique=True
)

# Sessions: fast lookup by lab + status
sessions_col.create_index(
    [("lab_id", ASCENDING), ("status", ASCENDING)]
)

# Survey responses: unique per student per session INSTANCE (not session_id)
# This allows the same student to submit for SW1 morning AND SW1 afternoon
survey_responses_col.create_index(
    [("student_id", ASCENDING), ("session_instance_id", ASCENDING)],
    unique=True,
    sparse=True  # sparse so docs without session_instance_id aren't affected
)

# Admins: unique email
admins_col.create_index(
    [("email", ASCENDING)],
    unique=True
)