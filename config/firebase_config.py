# """
# Firebase configuration.
# Place your serviceAccountKey.json in the config/ folder.
# Update FIREBASE_CONFIG with your project's web app credentials.
# """

# import firebase_admin
# from firebase_admin import credentials, firestore, storage, auth
# import os

# # ─── Pyrebase config (client-side auth for teacher/student login) ───────────
# # Replace these values with your Firebase project's web config
# FIREBASE_CONFIG = {
#     "apiKey": "YOUR_API_KEY",
#     "authDomain": "YOUR_PROJECT_ID.firebaseapp.com",
#     "projectId": "YOUR_PROJECT_ID",
#     "storageBucket": "YOUR_PROJECT_ID.appspot.com",
#     "messagingSenderId": "YOUR_SENDER_ID",
#     "appId": "YOUR_APP_ID",
#     "databaseURL": ""  # Leave empty if not using Realtime DB
# }

# # ─── Admin SDK init (server-side) ───────────────────────────────────────────
# _admin_initialized = False

# def init_firebase_admin():
#     global _admin_initialized
#     if _admin_initialized:
#         return

#     service_key = os.path.join(os.path.dirname(__file__), "serviceAccountKey.json")
#     if not os.path.exists(service_key):
#         raise FileNotFoundError(
#             "serviceAccountKey.json not found in config/.\n"
#             "Download it from Firebase Console → Project Settings → Service Accounts."
#         )

#     cred = credentials.Certificate(service_key)
#     firebase_admin.initialize_app(cred, {
#         "storageBucket": FIREBASE_CONFIG["storageBucket"]
#     })
#     _admin_initialized = True

# def get_firestore():
#     init_firebase_admin()
#     return firestore.client()

# def get_storage():
#     init_firebase_admin()
#     return storage.bucket()

# def get_auth():
#     init_firebase_admin()
#     return auth



import firebase_admin
from firebase_admin import credentials, firestore, storage, auth
import os

# 🔥 Firebase Web Config
FIREBASE_CONFIG = {
    "apiKey": "AIzaSyDZRUsUOCygK7ntsuF642Io82XJi5THT-Y",
    "authDomain": "face-attendance-project-5e255.firebaseapp.com",
    "projectId": "face-attendance-project-5e255",
    "storageBucket": "face-attendance-project-5e255.appspot.com",
    "messagingSenderId": "257562660071",
    "appId": "1:257562660071:web:4d06c98622a659ca742642",
    "measurementId": "G-GVEQ7ZNXQS"
}

# ✅ REQUIRED (YOU MISSED THIS)
_admin_initialized = False


# 🔥 INIT FIREBASE
def init_firebase_admin():
    global _admin_initialized

    if _admin_initialized:
        return

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    service_key_path = os.path.join(BASE_DIR, "config", "serviceAccountKey.json")

    print("Firebase key path:", service_key_path)

    if not os.path.exists(service_key_path):
        raise FileNotFoundError("serviceAccountKey.json not found")

    cred = credentials.Certificate(service_key_path)

    firebase_admin.initialize_app(cred, {
        "storageBucket": FIREBASE_CONFIG["storageBucket"]
    })

    _admin_initialized = True
    print("Firebase initialized")


    # 🔥 FIRESTORE
def get_firestore():
    init_firebase_admin()
    return firestore.client()


# 🔥 STORAGE
def get_storage():
    init_firebase_admin()
    return storage.bucket()


# 🔥 AUTH
def get_auth():
    init_firebase_admin()
    return auth