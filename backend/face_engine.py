import cv2
import numpy as np
import face_recognition

def encode_face_from_bytes(image_bytes):
    """
    Decodes image bytes, detects face, and returns a 128D encoding list.
    """
    try:
        # Convert bytes to numpy array
        np_arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        if img is None:
            return None

        # Convert BGR (OpenCV) to RGB (face_recognition)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Find face locations and encodings
        locations = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, locations)

        if not encodings:
            return None

        # Return the first face's encoding as a list of floats
        return encodings[0].tolist()
    except Exception as e:
        print(f"Error encoding face: {e}")
        return None


def run_attendance_scan():
    """
    Standard webcam scan loop (Legacy/Utility)
    """
    cap = cv2.VideoCapture(0)
    print("Webcam starting for test scan...")
    
    while True:
        ret, frame = cap.read()
        if not ret: break

        # Mirror for display
        display_frame = cv2.flip(frame, 1)
        
        cv2.putText(display_frame, "Press 'Q' to exit Test Mode", (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.imshow("FaceAttend - Webcam Test", display_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()