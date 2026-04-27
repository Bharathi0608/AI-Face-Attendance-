"""
utils/helpers.py
Shared utility functions used across the project.
"""

import re
import os
import uuid
import json
import base64
import hashlib
from datetime import datetime, date, timedelta
from typing import Optional


# ═══════════════════════════════════════════════════════════
#  VALIDATION
# ═══════════════════════════════════════════════════════════

def is_valid_email(email: str) -> bool:
    """Basic email format validation."""
    pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))


def is_valid_password(password: str) -> tuple[bool, str]:
    """
    Validate password strength.
    Returns (is_valid, error_message).
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters."
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number."
    return True, ""


def sanitize_name(name: str) -> str:
    """Trim and title-case a name."""
    return " ".join(name.strip().split()).title()


def sanitize_roll(roll: str) -> str:
    """Uppercase roll number, strip whitespace."""
    return roll.strip().upper()


# ═══════════════════════════════════════════════════════════
#  DATE / TIME
# ═══════════════════════════════════════════════════════════

def today_iso() -> str:
    return date.today().isoformat()


def now_iso() -> str:
    return datetime.utcnow().isoformat()


def format_date_display(iso_date: str) -> str:
    """'2024-09-15' → 'Sep 15, 2024'"""
    try:
        d = date.fromisoformat(iso_date)
        return d.strftime("%b %d, %Y")
    except Exception:
        return iso_date


def date_range(start_iso: str, end_iso: str) -> list[str]:
    """Generate list of ISO date strings between two dates (inclusive)."""
    start = date.fromisoformat(start_iso)
    end   = date.fromisoformat(end_iso)
    result = []
    current = start
    while current <= end:
        result.append(current.isoformat())
        current += timedelta(days=1)
    return result


# ═══════════════════════════════════════════════════════════
#  ENCODING / IMAGES
# ═══════════════════════════════════════════════════════════

def image_bytes_to_base64(image_bytes: bytes) -> str:
    """Convert raw image bytes to base64 data URI (JPEG)."""
    encoded = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:image/jpeg;base64,{encoded}"


def base64_to_bytes(data_uri: str) -> bytes:
    """Convert base64 data URI to raw bytes."""
    if "," in data_uri:
        data_uri = data_uri.split(",", 1)[1]
    return base64.b64decode(data_uri)


def allowed_image_file(filename: str) -> bool:
    allowed = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}
    ext = os.path.splitext(filename.lower())[1]
    return ext in allowed


# ═══════════════════════════════════════════════════════════
#  STATISTICS
# ═══════════════════════════════════════════════════════════

def attendance_percentage(present: int, total: int) -> float:
    if total == 0:
        return 0.0
    return round((present / total) * 100, 1)


def compute_student_stats(records: list[dict]) -> dict:
    """
    Given a list of attendance record dicts with 'status' key,
    return {total, present, absent, percentage}.
    """
    total   = len(records)
    present = sum(1 for r in records if r.get("status") == "present")
    absent  = total - present
    return {
        "total":      total,
        "present":    present,
        "absent":     absent,
        "percentage": attendance_percentage(present, total)
    }


# ═══════════════════════════════════════════════════════════
#  MISC
# ═══════════════════════════════════════════════════════════

def generate_id(prefix: str = "", length: int = 8) -> str:
    """Generate a short random uppercase ID."""
    uid = uuid.uuid4().hex[:length].upper()
    return f"{prefix}{uid}" if prefix else uid


def mask_email(email: str) -> str:
    """'teacher@gmail.com' → 'te****@gmail.com'"""
    parts = email.split("@")
    if len(parts) != 2:
        return email
    name, domain = parts
    masked = name[:2] + ("*" * max(2, len(name) - 2))
    return f"{masked}@{domain}"


def safe_json_load(text: str, default=None):
    """Parse JSON safely, returning default on error."""
    try:
        return json.loads(text)
    except Exception:
        return default
