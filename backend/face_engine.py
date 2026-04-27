# import cv2
# import numpy as np

# # Load face detector
# face_cascade = cv2.CascadeClassifier(
#     cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
# )

# # Create recognizer
# recognizer = cv2.face.LBPHFaceRecognizer_create()

# # Dummy training data (you can improve later)
# faces = []
# labels = []

# def encode_face_from_bytes(image_bytes):
#     np_arr = np.frombuffer(image_bytes, np.uint8)
#     img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     faces_detected = face_cascade.detectMultiScale(gray, 1.3, 5)

#     encodings = []
#     for (x, y, w, h) in faces_detected:
#         face = gray[y:y+h, x:x+w]
#         encodings.append(face)

#         return encodings


# def run_attendance_scan():
#     cap = cv2.VideoCapture(0)

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#         faces_detected = face_cascade.detectMultiScale(gray, 1.3, 5)

#         for (x, y, w, h) in faces_detected:
#             cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
#             cv2.putText(frame, "Face Detected", (x, y-10),
#             cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

#             cv2.imshow("Attendance System", frame)

#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#             cap.release()
#             cv2.destroyAllWindows()


import cv2
import numpy as np

# Load face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def encode_face_from_bytes(image_bytes):
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if img is None:
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    encodings = []

    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        encodings.append(face)

        if len(encodings) == 0:
            return None

        return encodings


def run_attendance_scan():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces_detected = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces_detected:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, "Face Detected", (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

            cv2.imshow("Attendance System", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            cap.release()
            cv2.destroyAllWindows()