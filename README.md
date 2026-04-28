# 🎓 FaceAttend — AI Face Recognition Attendance System

A complete AI-powered attendance system using **Python**, **Flask**, **Firebase**, and **face_recognition**.  
Three separate portals — Admin, Teacher, Student — with real-time webcam face scanning.

---

## ✨ Features

| Portal | What it can do |
|--------|---------------|
| **Admin** | Login with hardcoded credentials · Add/delete teachers (creates Firebase Auth account) · Add/delete students with face photo registration · Create classes · Enroll students into classes |
| **Teacher** | Login with Gmail + password (assigned by admin) · View assigned classes · View daily attendance records |
| **Student** | Select active class · Trigger face scan · See present/absent result in real time |

---

## 🛠 Tech Stack

- **Backend**: Python 3.10+, Flask 3.0
- **Face Recognition**: `face_recognition` (dlib) + OpenCV
- **Database**: Firebase Firestore
- **Auth**: Firebase Authentication (email/password)
- **Storage**: Firebase Storage (face photos)
- **Frontend**: HTML/CSS/JS (dark theme, no frameworks needed)

---

## 📁 Project Structure

```
face_attendance/
├── app.py                        # Flask server (entry point)
├── requirements.txt
├── .env.example                  # Copy to .env and fill values
├── .gitignore
│
├── config/
│   └── firebase_config.py        # Firebase init (Admin SDK + Pyrebase)
│
├── backend/
│   ├── face_engine.py            # Face detection, encoding, recognition
│   ├── firebase_service.py       # All Firestore/Auth/Storage operations
│   └── routes_extra.py           # CSV export & stats API routes
│
├── utils/
│   ├── helpers.py                # Validators, formatters, utilities
│   └── reports.py                # CSV report builders
│
├── templates/
│   ├── index.html                # Landing page (portal selector)
│   ├── admin.html                # Admin dashboard
│   ├── teacher.html              # Teacher dashboard
│   └── student.html              # Student face-scan portal
│
└── scripts/
    ├── run_attendance_scan.py    # CLI scanner (standalone)
    ├── register_face.py          # Register/update student face via webcam
    └── seed_demo_data.py         # Seed Firebase with demo data
```

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone <your-repo-url>
cd face_attendance

# Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

> **Note on `face_recognition`**: It requires `cmake` and `dlib`.
> ```bash
> # Ubuntu/Debian:
> sudo apt-get install cmake libopenblas-dev liblapack-dev
>
> # macOS:
> brew install cmake
>
> # Windows: Install cmake from cmake.org, then pip install dlib
> ```

---

### 2. Firebase Setup

1. Go to [Firebase Console](https://console.firebase.google.com) → **Create Project**
2. Enable **Authentication** → Sign-in method → **Email/Password**
3. Create **Firestore Database** (start in test mode)
4. Create **Storage** bucket
5. Go to **Project Settings → Service Accounts** → Generate new private key → Save as `config/serviceAccountKey.json`
6. Go to **Project Settings → General → Your apps → Web** → Copy the config values

---

### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env`:
```env
SECRET_KEY=your_random_secret_key

FIREBASE_API_KEY=AIza...
FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_STORAGE_BUCKET=your-project-id.appspot.com
FIREBASE_MESSAGING_SENDER_ID=123456789
FIREBASE_APP_ID=1:123:web:abc123
```

Also update `config/firebase_config.py` `FIREBASE_CONFIG` dict with the same values.

---

### 4. Run the Server

```bash
python app.py
```

Open your browser:
- **Home**: http://localhost:5000/
- **Admin**: http://localhost:5000/admin  → `admin@gmail.com` / `Admin@123`
- **Teacher**: http://localhost:5000/teacher
- **Student**: http://localhost:5000/student

---

## 👤 Workflow

### Admin adds a Teacher
1. Go to `/admin` → Login
2. Click **Teachers** → **Add Teacher**
3. Fill name, email, subject, password → Submit
4. Firebase Auth account is created automatically

### Admin adds a Student
1. Go to **Students** → **Add Student**
2. Fill name, roll number, email
3. Upload a clear frontal face photo
4. Face encoding is extracted and stored in Firestore

### Admin creates a Class & enrolls students
1. Go to **Classes** → **Create Class**
2. Assign a teacher, set schedule
3. Click **Enroll** button next to the class
4. Select a student and click Enroll

### Teacher takes attendance
1. Go to `/teacher` → Login with Gmail/password
2. Click **Take Attendance** → Select class → Click **Start Face Scan**
3. Webcam opens on the server machine
4. Each recognized student → marked **Present**
5. Unrecognized students → marked **Absent**
6. View results under **Attendance Records**

### From command line (alternative)
```bash
python scripts/run_attendance_scan.py --class_id ABC12345 --seconds 30
```

---

## 🧪 Demo / Testing

Seed Firebase with demo teachers, students and classes:
```bash
python scripts/seed_demo_data.py
```

Register a student's face via webcam:
```bash
# List students to find UIDs
python scripts/register_face.py --list

# Register via webcam (press SPACE 3 times)
python scripts/register_face.py --student_uid <UID>

# Or from image file
python scripts/register_face.py --student_uid <UID> --image photo.jpg
```

---

## 🔌 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/admin/login` | Admin login |
| POST | `/api/teacher/login` | Teacher login (Firebase Auth) |
| GET  | `/api/teachers` | List all teachers |
| POST | `/api/teachers` | Add teacher |
| DELETE | `/api/teachers/<uid>` | Delete teacher |
| GET  | `/api/students` | List all students |
| POST | `/api/students` | Add student (multipart with face_image) |
| DELETE | `/api/students/<uid>` | Delete student |
| GET  | `/api/classes` | List all classes |
| POST | `/api/classes` | Create class |
| POST | `/api/classes/<id>/enroll` | Enroll student in class |
| DELETE | `/api/classes/<id>` | Delete class |
| POST | `/api/attendance/scan` | Start face-recognition scan |
| POST | `/api/attendance/manual` | Manual mark attendance |
| GET  | `/api/teacher/<uid>/attendance` | Get attendance records |
| GET  | `/api/export/daily` | Download daily CSV |
| GET  | `/api/export/summary` | Download summary CSV |
| GET  | `/api/stats/class/<id>` | Class attendance stats |
| GET  | `/api/health` | Health check |

---

## ⚙️ Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `ADMIN_EMAIL` | `admin@gmail.com` | Admin login email |
| `ADMIN_PASSWORD` | `Admin@123` | Admin login password |
| `FACE_TOLERANCE` | `0.50` | Lower = stricter match (0.0–1.0) |
| `DEFAULT_SCAN_SECONDS` | `10` | Webcam scan duration |
| `FLASK_PORT` | `5000` | Server port |
| `FLASK_DEBUG` | `true` | Debug mode |

---

## 🔒 Security Notes

- Never commit `config/serviceAccountKey.json` or `.env` (both in `.gitignore`)
- Change `ADMIN_PASSWORD` and `SECRET_KEY` before deploying
- In production set `FLASK_DEBUG=false`
- Firebase Storage rules should restrict public read to face images only
- Consider rate-limiting the `/api/attendance/scan` endpoint

---

## 🐛 Troubleshooting

**`face_recognition` install fails**
```bash
pip install cmake
pip install dlib
pip install face_recognition
```

**`No face detected` on student upload**  
Use a high-resolution, well-lit frontal face photo. Avoid sunglasses, masks, or extreme angles.

**Webcam not opening**  
Check camera index: `python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"`  
If `False`, try index `1` or `2`.

**Firebase auth error**  
Make sure `FIREBASE_CONFIG` in `firebase_config.py` matches your web app config (not the service account).

**`serviceAccountKey.json` not found**  
Download from Firebase Console → Project Settings → Service Accounts → Generate new private key.
