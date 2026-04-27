"""
scripts/seed_demo_data.py

Seeds Firebase with demo data for testing:
  - 2 teachers
  - 4 students (no real faces — uses placeholder encodings)
  - 2 classes with students enrolled

Run:  python scripts/seed_demo_data.py

WARNING: This creates real Firebase records. Use only on a dev project.
"""

import sys
import os
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.firebase_service import (
    add_teacher, get_all_teachers,
    create_class, get_all_classes,
    enroll_student_in_class,
    get_firestore
)
from config.firebase_config import get_firestore
import uuid
from datetime import datetime


def seed_student_no_photo(name, email, roll, fake_encoding=None):
    """Add a student without a real photo (for demo/testing)."""
    db = get_firestore()
    uid = str(uuid.uuid4())
    encoding = fake_encoding if fake_encoding else np.random.rand(128).tolist()
    data = {
        "uid": uid,
        "name": name,
        "email": email,
        "roll_number": roll,
        "role": "student",
        "face_encoding": encoding,
        "image_url": "",
        "class_ids": [],
        "created_at": datetime.utcnow().isoformat()
    }
    db.collection("users").document(uid).set(data)
    print(f"  ✅ Student: {name} ({roll}) — uid: {uid[:8]}…")
    return data


def main():
    print("\n" + "="*55)
    print("  FaceAttend — Demo Data Seeder")
    print("="*55)

    # ─── Teachers ───
    print("\n👩‍🏫  Creating teachers…")
    teachers = [
        {"name": "Dr. Priya Sharma",  "email": "priya.sharma@school.edu",  "password": "Teacher@123", "subject": "Computer Science"},
        {"name": "Prof. Arjun Mehta", "email": "arjun.mehta@school.edu",   "password": "Teacher@123", "subject": "Mathematics"},
    ]
    teacher_uids = []
    for t in teachers:
        try:
            result = add_teacher(**t)
            teacher_uids.append(result["uid"])
            print(f"  ✅ {t['name']} ({t['email']})")
        except Exception as e:
            print(f"  ⚠  {t['name']} — {e} (might already exist)")
            existing = [x for x in get_all_teachers() if x["email"] == t["email"]]
            if existing:
                teacher_uids.append(existing[0]["uid"])

    if len(teacher_uids) < 2:
        print("\n❌ Could not create/find 2 teachers. Aborting.")
        return

    # ─── Students ───
    print("\n👤  Creating demo students (no real face photos)…")
    students_data = [
        {"name": "Alice Kumar",    "email": "alice@college.edu",   "roll": "CS001"},
        {"name": "Bob Rajan",      "email": "bob@college.edu",     "roll": "CS002"},
        {"name": "Carol Nair",     "email": "carol@college.edu",   "roll": "CS003"},
        {"name": "David Singh",    "email": "david@college.edu",   "roll": "CS004"},
        {"name": "Eva Patel",      "email": "eva@college.edu",     "roll": "MA001"},
        {"name": "Frank Thomas",   "email": "frank@college.edu",   "roll": "MA002"},
    ]
    student_records = []
    for s in students_data:
        rec = seed_student_no_photo(s["name"], s["email"], s["roll"])
        student_records.append(rec)

    # ─── Classes ───
    print("\n📚  Creating classes…")
    classes_data = [
        {"name": "Data Structures & Algorithms", "teacher_uid": teacher_uids[0], "schedule": "Mon/Wed 9:00–10:30 AM"},
        {"name": "Calculus II",                   "teacher_uid": teacher_uids[1], "schedule": "Tue/Thu 11:00 AM–12:30 PM"},
    ]
    class_ids = []
    for c in classes_data:
        try:
            result = create_class(**c)
            class_ids.append(result["class_id"])
            print(f"  ✅ {c['name']} — ID: {result['class_id']}")
        except Exception as e:
            print(f"  ⚠  {c['name']} — {e}")

    # ─── Enroll ───
    if len(class_ids) >= 2:
        print("\n📎  Enrolling students into classes…")
        # First 4 students → CS class
        for s in student_records[:4]:
            try:
                enroll_student_in_class(s["uid"], class_ids[0])
                print(f"  ✅ {s['name']} → {class_ids[0]}")
            except Exception as e:
                print(f"  ⚠  {e}")
        # Last 2 students → Math class
        for s in student_records[4:]:
            try:
                enroll_student_in_class(s["uid"], class_ids[1])
                print(f"  ✅ {s['name']} → {class_ids[1]}")
            except Exception as e:
                print(f"  ⚠  {e}")

    print("\n" + "="*55)
    print("  Seeding complete!")
    print("\n  Teacher logins:")
    for t in teachers:
        print(f"    Email: {t['email']}")
        print(f"    Pass:  {t['password']}")
    print("\n  Admin login:")
    print("    Email: admin@school.edu")
    print("    Pass:  Admin@1234")
    print("="*55 + "\n")


if __name__ == "__main__":
    main()
