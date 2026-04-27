import os
import face_recognition
import numpy as np
import cv2
from backend.firebase_service import get_firestore

db = get_firestore()
users_ref = db.collection('users')
docs = users_ref.where('role', '==', 'student').stream()

updated = 0
failed = 0

for doc in docs:
    data = doc.to_dict()
    uid = doc.id
    
    # Check if encoding is missing or empty
    enc = data.get('face_encoding')
    if enc:
        continue
        
    image_url = data.get('image_url')
    if not image_url:
        print(f"User {uid} ({data.get('name')}) has no image_url")
        continue
        
    # Example image_url: /uploads/abc-123_photo.jpeg
    filename = os.path.basename(image_url)
    filepath = os.path.join("uploads", filename)
    
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        continue
        
    print(f"Processing {data.get('name')} ({filename})...")
    
    img = cv2.imread(filepath)
    if img is None:
        print(f"Failed to read image {filepath}")
        continue
        
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    encodings = face_recognition.face_encodings(rgb_img)
    
    if encodings:
        face_encoding = encodings[0].tolist()
        users_ref.document(uid).update({'face_encoding': face_encoding})
        print(f"✅ Updated face_encoding for {data.get('name')}")
        updated += 1
    else:
        print(f"❌ No face detected in image for {data.get('name')}")
        failed += 1

print(f"Done! Updated {updated} students, failed {failed}.")
