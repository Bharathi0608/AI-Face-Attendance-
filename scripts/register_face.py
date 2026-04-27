"""
scripts/register_face.py

Register a student's face directly from the webcam
(or from an existing image file).

Usage:
    # From webcam - takes 3 photos and averages encodings:
    python scripts/register_face.py --student_uid <UID>

    # From image file:
    python scripts/register_face.py --student_uid <UID> --image path/to/photo.jpg

    # List all students to find UIDs:
    python scripts/register_face.py --list
"""

import sys
import os
import argparse
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cv2
import face_recognition
from backend.firebase_service import get_all_students, get_firestore


def capture_face_from_webcam(num_samples: int = 3) -> list:
    """
    Open webcam, wait for a clear face, capture `num_samples` encodings,
    return average encoding as list.
    Press SPACE to capture, Q to quit.
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Cannot open webcam.")

    encodings = []
    print(f"\n  📷  Webcam open. Press SPACE to capture ({num_samples} needed). Press Q to quit.\n")

    while len(encodings) < num_samples:
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        locations = face_recognition.face_locations(rgb)

        display = frame.copy()
        if locations:
            top, right, bottom, left = locations[0]
            cv2.rectangle(display, (left, top), (right, bottom), (0, 200, 100), 2)
            cv2.putText(display, f"Face detected! ({len(encodings)}/{num_samples} captured)",
                       (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 100), 1)
        else:
            cv2.putText(display, "No face detected — adjust position",
                       (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 80, 220), 2)

        cv2.imshow("Face Registration — Press SPACE to capture", display)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        if key == ord(' ') and locations:
            enc = face_recognition.face_encodings(rgb, locations)
            if enc:
                encodings.append(enc[0])
                print(f"  ✅  Sample {len(encodings)}/{num_samples} captured.")

    cap.release()
    cv2.destroyAllWindows()

    if not encodings:
        raise ValueError("No face samples captured.")

    avg_encoding = np.mean(encodings, axis=0)
    return avg_encoding.tolist()


def register_from_file(filepath: str) -> list:
    """Extract face encoding from image file."""
    img = face_recognition.load_image_file(filepath)
    locations = face_recognition.face_locations(img)
    if not locations:
        raise ValueError(f"No face found in '{filepath}'.")
    encodings = face_recognition.face_encodings(img, locations)
    if not encodings:
        raise ValueError(f"Could not encode face in '{filepath}'.")
    return encodings[0].tolist()


def update_student_encoding(student_uid: str, encoding: list):
    """Update face_encoding in Firestore for a student."""
    db = get_firestore()
    db.collection("users").document(student_uid).update({"face_encoding": encoding})


def list_students():
    students = get_all_students()
    if not students:
        print("No students found.")
        return
    print(f"\n{'UID':<40} {'Name':<25} {'Roll':<12} {'Has Face'}")
    print("-" * 90)
    for s in students:
        has_face = "✅" if s.get("face_encoding") else "❌"
        print(f"  {s['uid']:<38} {s['name']:<25} {s.get('roll_number','—'):<12} {has_face}")
    print()


def main():
    parser = argparse.ArgumentParser(description="FaceAttend — Face Registration Tool")
    parser.add_argument("--student_uid", help="Student UID to register face for")
    parser.add_argument("--image",       help="Path to image file (optional; uses webcam if omitted)")
    parser.add_argument("--list",        action="store_true", help="List all students and their UIDs")
    args = parser.parse_args()

    print("\n" + "="*55)
    print("  FaceAttend — Face Registration")
    print("="*55)

    if args.list:
        list_students()
        return

    if not args.student_uid:
        print("❌  --student_uid required (or use --list to find UIDs)")
        parser.print_help()
        sys.exit(1)

    # Find student
    students = get_all_students()
    student = next((s for s in students if s["uid"] == args.student_uid), None)
    if not student:
        print(f"❌  Student with uid '{args.student_uid}' not found.")
        sys.exit(1)

    print(f"\n  Student: {student['name']} ({student.get('roll_number','—')})")
    print(f"  UID:     {student['uid']}\n")

    try:
        if args.image:
            print(f"  📁  Loading from file: {args.image}")
            encoding = register_from_file(args.image)
        else:
            encoding = capture_face_from_webcam(num_samples=3)

        print("\n  💾  Saving encoding to Firebase…")
        update_student_encoding(student["uid"], encoding)
        print(f"  ✅  Face registered successfully for {student['name']}!\n")

    except Exception as e:
        print(f"\n  ❌  Error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
