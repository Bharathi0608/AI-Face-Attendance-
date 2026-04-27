# """
# scripts/run_attendance_scan.py

# Standalone script to run a face-recognition attendance scan
# directly on the machine with the webcam (no Flask needed).

# Usage:
#     python scripts/run_attendance_scan.py --class_id ABC12345 --seconds 30

# This is useful when the webcam is on the same machine as the server
# but you want to trigger scans from the command line.
# """

# import sys
# import os
# import argparse

# # Allow imports from project root
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from backend.firebase_service import (
#     get_student_encodings_for_class,
#     get_all_students,
#     mark_attendance,
#     get_all_classes
# )
# from backend.face_engine import run_attendance_scan
# import cv2


# def main():
#     parser = argparse.ArgumentParser(description="Face Recognition Attendance Scanner")
#     parser.add_argument("--class_id",  required=True, help="Class ID to take attendance for")
#     parser.add_argument("--seconds",   type=int, default=30, help="Scan duration in seconds (default: 30)")
#     parser.add_argument("--tolerance", type=float, default=0.50, help="Face match tolerance 0.0–1.0 (default: 0.50)")
#     parser.add_argument("--camera",    type=int, default=0, help="Camera device index (default: 0)")
#     args = parser.parse_args()

#     print("\n" + "="*55)
#     print("  FaceAttend — Attendance Scanner")
#     print("="*55)

#     # Verify class exists
#     all_classes = get_all_classes()
#     cls_info = next((c for c in all_classes if c["class_id"] == args.class_id), None)
#     if not cls_info:
#         print(f"\n❌  Class '{args.class_id}' not found in Firebase.")
#         print("    Available classes:", [c["class_id"] for c in all_classes])
#         sys.exit(1)

#     print(f"\n📚  Class    : {cls_info['name']} ({args.class_id})")
#     print(f"⏱   Duration : {args.seconds} seconds")
#     print(f"🎯  Tolerance: {args.tolerance}")

#     # Load face encodings
#     print("\n⬇   Loading face encodings from Firebase…")
#     known_encodings = get_student_encodings_for_class(args.class_id)
#     if not known_encodings:
#         print("❌  No students with face data enrolled in this class.")
#         sys.exit(1)

#     students = {s["uid"]: s for s in get_all_students()}
#     name_map = {uid: students[uid]["name"] for uid in known_encodings if uid in students}

#     print(f"✅  Loaded {len(known_encodings)} student encoding(s):")
#     for uid, name in name_map.items():
#         print(f"    • {name}")

#     print(f"\n🎥  Opening camera (index {args.camera})…")
#     print("    Press  Q  to finish scan early.\n")

#     # Override camera index if needed
#     import backend.face_engine as fe
#     original_open = cv2.VideoCapture

#     # Run scan
#     attendance = run_attendance_scan(
#         known_encodings=known_encodings,
#         name_map=name_map,
#         scan_seconds=args.seconds,
#         tolerance=args.tolerance
#     )

#     # Save results
#     print("\n📝  Saving attendance to Firebase…\n")
#     print(f"{'Name':<25} {'Roll':<12} {'Status'}")
#     print("-" * 50)

#     for uid, status in attendance.items():
#         name = name_map.get(uid, uid)
#         roll = students.get(uid, {}).get("roll_number", "—")
#         icon = "✅" if status == "present" else "❌"
#         print(f"  {icon}  {name:<23} {roll:<12} {status.upper()}")
#         mark_attendance(args.class_id, uid, status)

#     present = sum(1 for s in attendance.values() if s == "present")
#     total   = len(attendance)
#     print("-" * 50)
#     print(f"\n  Present : {present}/{total}")
#     print(f"  Absent  : {total - present}/{total}")
#     print(f"  Rate    : {round(present/total*100, 1) if total else 0}%")
#     print("\n✅  Attendance saved successfully!\n")
    
    
#     def start_attendance(class_id, seconds=30):
#         print("🚀 Starting attendance for class:", class_id)

#     # get students + encodings
#     students = get_student_encodings_for_class(class_id)

#     if not students:
#         print("❌ No students found")
#         return {"success": False, "message": "No students found"}

#     # run face scan
#     results = run_attendance_scan(
#         students,
#         scan_seconds=seconds
#     )

#     # save attendance
#     for r in results:
#         student_uid = r["student_uid"]
#         status = "present" if r["matched"] else "absent"

#         mark_attendance(class_id, student_uid, status)

#         return {"success": True, "records": results}


# if __name__ == "__main__":
#     main()

"""
scripts/run_attendance_scan.py
"""

import sys
import os
import argparse
import cv2
import time

# Allow imports from project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.firebase_service import (
    get_student_encodings_for_class,
    get_all_students,
    mark_attendance,
    get_all_classes
)
from backend.face_engine import run_attendance_scan


# =========================
# 🔥 NEW FUNCTION FOR API
# =========================
def start_attendance(class_id, seconds=30):
    print("🚀 Starting webcam scan for class:", class_id)

    students = get_student_encodings_for_class(class_id)

    if not students:
        return {"success": False, "message": "No students found"}

    cap = cv2.VideoCapture(0)

    start_time = time.time()
    marked_students = set()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 🔥 Face detection
        results = run_attendance_scan(frame, students)

        for r in results:
            student_uid = r["student_uid"]

            if student_uid not in marked_students:
                status = "present" if r["matched"] else "absent"
                mark_attendance(class_id, student_uid, status)
                marked_students.add(student_uid)

                cv2.imshow("Face Attendance", frame)

                # Stop after time
                if time.time() - start_time > seconds:
                    break

                # Press Q to exit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                cap.release()
                cv2.destroyAllWindows()

                return {"success": True}


                # =========================
                # 🧠 EXISTING CLI FUNCTION (UNCHANGED)
                # =========================
def main():
    parser = argparse.ArgumentParser(description="Face Recognition Attendance Scanner")
    parser.add_argument("--class_id", required=True, help="Class ID")
    parser.add_argument("--seconds", type=int, default=30)
    parser.add_argument("--tolerance", type=float, default=0.50)
    parser.add_argument("--camera", type=int, default=0)
    args = parser.parse_args()

    print("\n" + "="*55)
    print("  FaceAttend — Attendance Scanner")
    print("="*55)

    all_classes = get_all_classes()
    cls_info = next((c for c in all_classes if c["class_id"] == args.class_id), None)

    if not cls_info:
        print("❌ Class not found")
        sys.exit(1)

        print(f"\n📚 Class: {cls_info['name']}")

        known_encodings = get_student_encodings_for_class(args.class_id)

        if not known_encodings:
            print("❌ No students")
            sys.exit(1)

            students = {s["uid"]: s for s in get_all_students()}

            print("\n🎥 Opening camera...")

            attendance = run_attendance_scan(
                known_encodings=known_encodings,
                name_map={uid: students[uid]["name"] for uid in known_encodings if uid in students},
                scan_seconds=args.seconds,
                tolerance=args.tolerance
            )

            for uid, status in attendance.items():
                mark_attendance(args.class_id, uid, status)

                print("\n✅ Attendance saved!")


if __name__ == "__main__":
    main()