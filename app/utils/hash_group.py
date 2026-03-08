# backend/app/utils/hash_group.py
import hashlib

def assign_experiment_group(student_id: str, session_id: str) -> str:
    """
    Deterministically assigns a student to control (30%) or treatment (70%) group
    per session/lab.
    """
    # Combine student_id and session_id for deterministic but per-session hash
    key = f"{student_id}_{session_id}"
    
    # MD5 hash → integer → modulo 10
    val = int(hashlib.md5(key.encode()).hexdigest(), 16) % 10
    
    # 0,1,2 → control (30%), 3-9 → treatment (70%)
    return "control" if val <= 2 else "treatment"