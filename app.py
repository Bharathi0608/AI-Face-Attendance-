# # # """
# # # app.py  —  FaceAttend Flask Application Entry Point
# # # Run:  python app.py
# # # """

# # # import sys
# # # import os

# # # try:
# # #     from dotenv import load_dotenv
# # #     load_dotenv()
# # # except ImportError:
# # #     pass

# # # sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# # # from flask import Flask, request, jsonify, render_template, session
# # # from flask_cors import CORS
# # # import threading

# # # from backend.firebase_service import (
# # #     add_teacher, get_all_teachers, delete_teacher,
# # #     add_student, get_all_students, delete_student,
# # #     create_class, get_all_classes, get_classes_for_teacher,
# # #     enroll_student_in_class, delete_class,
# # #     mark_attendance, get_attendance_for_class_date,
# # #     get_attendance_summary, get_student_encodings_for_class,
# # #     get_user_by_uid, verify_teacher_login
# # # )
# # # from backend.face_engine import encode_face_from_bytes, run_attendance_scan
# # # from backend.routes_extra import extra_bp

# # # app = Flask(__name__, template_folder="templates", static_folder="static")
# # # app.secret_key = os.environ.get("SECRET_KEY", "change_this_in_production_xyz")
# # # CORS(app)
# # # app.register_blueprint(extra_bp)

# # # ADMIN_EMAIL    = os.environ.get("ADMIN_EMAIL",    "admin@school.edu")
# # # ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "Admin@1234")


# # # # ── PAGE ROUTES ──────────────────────────────────────────────

# # # @app.route("/")
# # # def index():
# # #     return render_template("index.html")

# # # @app.route("/admin")
# # # def admin_page():
# # #     return render_template("admin.html")

# # # @app.route("/teacher")
# # # def teacher_page():
# # #     return render_template("teacher.html")

# # # @app.route("/student")
# # # def student_page():
# # #     return render_template("student.html")


# # # # ── AUTH ─────────────────────────────────────────────────────

# # # @app.route("/api/admin/login", methods=["POST"])
# # # def admin_login():
# # #     d = request.json or {}
# # #     if d.get("email") == ADMIN_EMAIL and d.get("password") == ADMIN_PASSWORD:
# # #         session["role"] = "admin"
# # #         return jsonify({"success": True, "message": "Admin logged in"})
# # #     return jsonify({"success": False, "message": "Invalid credentials"}), 401


# # # @app.route("/api/teacher/login", methods=["POST"])
# # # def teacher_login():
# # #     d = request.json or {}
# # #     try:
# # #         profile = verify_teacher_login(d["email"], d["password"])
# # #         session["role"] = "teacher"
# # #         session["uid"]  = profile["uid"]
# # #         return jsonify({"success": True, "profile": profile})
# # #     except PermissionError as e:
# # #         return jsonify({"success": False, "message": str(e)}), 403
# # #     except Exception:
# # #         return jsonify({"success": False, "message": "Invalid email or password"}), 401


# # # @app.route("/api/logout", methods=["POST"])
# # # def logout():
# # #     session.clear()
# # #     return jsonify({"success": True})


# # # # ── TEACHERS ─────────────────────────────────────────────────

# # # @app.route("/api/teachers", methods=["GET"])
# # # def list_teachers():
# # #     return jsonify(get_all_teachers())


# # # @app.route("/api/teachers", methods=["POST"])
# # # def create_teacher():
# # #     d = request.json or {}
# # #     try:
# # #         teacher = add_teacher(
# # #             name=d["name"], email=d["email"],
# # #             password=d["password"], subject=d.get("subject", "")
# # #         )
# # #         return jsonify({"success": True, "teacher": teacher})
# # #     except Exception as e:
# # #         return jsonify({"success": False, "message": str(e)}), 400


# # # @app.route("/api/teachers/<uid>", methods=["DELETE"])
# # # def remove_teacher(uid):
# # #     try:
# # #         delete_teacher(uid)
# # #         return jsonify({"success": True})
# # #     except Exception as e:
# # #         return jsonify({"success": False, "message": str(e)}), 400


# # # # ── STUDENTS ─────────────────────────────────────────────────

# # # @app.route("/api/students", methods=["GET"])
# # # def list_students():
# # #     return jsonify(get_all_students())


# # # @app.route("/api/students", methods=["POST"])
# # # def create_student():
# # #     name  = request.form.get("name", "").strip()
# # #     email = request.form.get("email", "").strip()
# # #     roll  = request.form.get("roll_number", "").strip()
# # #     file  = request.files.get("face_image")

# # #     if not all([name, email, roll, file]):
# # #         return jsonify({"success": False, "message": "All fields including face photo are required."}), 400

# # #     image_bytes = file.read()
# # #     encoding = encode_face_from_bytes(image_bytes)
# # #     if not encoding:
# # #         return jsonify({
# # #             "success": False,
# # #             "message": "No face detected in the uploaded image. Use a clear, well-lit frontal photo."
# # #         }), 400

# # #     try:
# # #         student = add_student(
# # #             name=name, email=email, roll_number=roll,
# # #             face_encoding=encoding,
# # #             image_bytes=image_bytes,
# # #             image_filename=file.filename or "face.jpg"
# # #         )
# # #         return jsonify({"success": True, "student": student})
# # #     except Exception as e:
# # #         return jsonify({"success": False, "message": str(e)}), 400


# # # @app.route("/api/students/<uid>", methods=["DELETE"])
# # # def remove_student(uid):
# # #     try:
# # #         delete_student(uid)
# # #         return jsonify({"success": True})
# # #     except Exception as e:
# # #         return jsonify({"success": False, "message": str(e)}), 400


# # # # ── CLASSES ──────────────────────────────────────────────────

# # # @app.route("/api/classes", methods=["GET"])
# # # def list_classes():
# # #     return jsonify(get_all_classes())


# # # @app.route("/api/classes", methods=["POST"])
# # # def make_class():
# # #     d = request.json or {}
# # #     try:
# # #         cls = create_class(
# # #             name=d["name"],
# # #             teacher_uid=d["teacher_uid"],
# # #             schedule=d.get("schedule", "")
# # #         )
# # #         return jsonify({"success": True, "class": cls})
# # #     except Exception as e:
# # #         return jsonify({"success": False, "message": str(e)}), 400


# # # @app.route("/api/classes/<class_id>/enroll", methods=["POST"])
# # # def enroll(class_id):
# # #     d = request.json or {}
# # #     try:
# # #         enroll_student_in_class(d["student_uid"], class_id)
# # #         return jsonify({"success": True})
# # #     except Exception as e:
# # #         return jsonify({"success": False, "message": str(e)}), 400


# # # @app.route("/api/classes/<class_id>", methods=["DELETE"])
# # # def remove_class(class_id):
# # #     try:
# # #         delete_class(class_id)
# # #         return jsonify({"success": True})
# # #     except Exception as e:
# # #         return jsonify({"success": False, "message": str(e)}), 400


# # # # ── TEACHER DATA ─────────────────────────────────────────────

# # # @app.route("/api/teacher/<uid>/classes", methods=["GET"])
# # # def teacher_classes(uid):
# # #     return jsonify(get_classes_for_teacher(uid))


# # # @app.route("/api/teacher/<uid>/attendance", methods=["GET"])
# # # def teacher_attendance(uid):
# # #     class_id = request.args.get("class_id")
# # #     day      = request.args.get("date")
# # #     if not class_id:
# # #         return jsonify({"error": "class_id required"}), 400
# # #     records  = get_attendance_for_class_date(class_id, day)
# # #     students = {s["uid"]: s for s in get_all_students()}
# # #     for r in records:
# # #         info = students.get(r.get("student_uid"), {})
# # #         r["name"]        = info.get("name", "Unknown")
# # #         r["roll_number"] = info.get("roll_number", "—")
# # #     return jsonify(records)


# # # @app.route("/api/teacher/<uid>/summary", methods=["GET"])
# # # def teacher_summary(uid):
# # #     class_id = request.args.get("class_id")
# # #     if not class_id:
# # #         return jsonify({"error": "class_id required"}), 400
# # #     return jsonify(get_attendance_summary(class_id))


# # # # ── FACE SCAN ────────────────────────────────────────────────

# # # @app.route("/api/attendance/scan", methods=["POST"])
# # # def start_scan():
# # #     d = request.json or {}
# # #     class_id     = d.get("class_id")
# # #     scan_seconds = int(d.get("scan_seconds", 30))

# # #     if not class_id:
# # #         return jsonify({"success": False, "message": "class_id required"}), 400

# # #     known_encodings = get_student_encodings_for_class(class_id)
# # #     if not known_encodings:
# # #         return jsonify({"success": False,
# # #                         "message": "No enrolled students with face data found for this class."}), 400

# # #     students = {s["uid"]: s for s in get_all_students()}
# # #     name_map = {uid: students[uid]["name"] for uid in known_encodings if uid in students}

# # #     def scan_and_save():
# # #         try:
# # #             attendance = run_attendance_scan(
# # #                 known_encodings=known_encodings,
# # #                 name_map=name_map,
# # #                 scan_seconds=scan_seconds,
# # #                 tolerance=float(os.environ.get("FACE_TOLERANCE", "0.50"))
# # #             )
# # #             for uid, status in attendance.items():
# # #                 mark_attendance(class_id, uid, status)
# # #             print(f"[SCAN COMPLETE] {class_id}: {attendance}")
# # #         except Exception as ex:
# # #             print(f"[SCAN ERROR] {ex}")

# # #     t = threading.Thread(target=scan_and_save, daemon=True)
# # #     t.start()

# # #     return jsonify({
# # #         "success": True,
# # #         "message": (
# # #             f"Face scan started for {len(known_encodings)} student(s). "
# # #             f"Webcam will open on the server. Press Q or wait {scan_seconds}s to finish."
# # #         )
# # #     })


# # # @app.route("/api/attendance/manual", methods=["POST"])
# # # def manual_mark():
# # #     d = request.json or {}
# # #     try:
# # #         mark_attendance(
# # #             class_id=d["class_id"],
# # #             student_uid=d["student_uid"],
# # #             status=d["status"]
# # #         )
# # #         return jsonify({"success": True})
# # #     except Exception as e:
# # #         return jsonify({"success": False, "message": str(e)}), 400


# # # @app.route("/api/health", methods=["GET"])
# # # def health():
# # #     return jsonify({"status": "ok", "service": "FaceAttend", "version": "1.0.0"})


# # # # ── MAIN ─────────────────────────────────────────────────────

# # # if __name__ == "__main__":
# # #     port  = int(os.environ.get("FLASK_PORT", 5000))
# # #     debug = os.environ.get("FLASK_DEBUG", "true").lower() == "true"

# # #     print("\n" + "="*55)
# # #     print("  FaceAttend — AI Attendance System")
# # #     print("="*55)
# # #     print(f"  Home    -> http://localhost:{port}/")
# # #     print(f"  Admin   -> http://localhost:{port}/admin")
# # #     print(f"  Teacher -> http://localhost:{port}/teacher")
# # #     print(f"  Student -> http://localhost:{port}/student")
# # #     print("-"*55)
# # #     print(f"  Admin: {ADMIN_EMAIL} / {ADMIN_PASSWORD}")
# # #     print("="*55 + "\n")

# # #     app.run(debug=debug, host="0.0.0.0", port=port, threaded=True)

# # """
# # app.py  —  FaceAttend Flask Application Entry Point
# # Run:  python app.py
# # """

# # import sys
# # import os
# # import webbrowser
# # import threading
# # from backend.routes_extra import extra_bp

# # # Load .env
# # try:
# #     from dotenv import load_dotenv
# #     load_dotenv()
# # except ImportError:
# #     pass

# # sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# # from flask import Flask, request, jsonify, render_template, session
# # from backend.firebase_service import get_all_teachers
# # from backend.firebase_service import add_teacher, add_student
# # from backend.firebase_service import get_all_students
# # from flask_cors import CORS
# # from flask import send_from_directory

# # # from backend.firebase_service import (
# # #     add_teacher, get_all_teachers, delete_teacher,
# # #     add_student, get_all_students, delete_student,
# # #     create_class, get_all_classes,
# # #     enroll_student_in_class, delete_class,
# # #     mark_attendance, get_attendance_for_class_date,
# # #     get_attendance_summary, get_student_encodings_for_class,
# # #     get_user_by_uid, verify_teacher_login
# # # )

# # from backend.face_engine import encode_face_from_bytes, run_attendance_scan
# # from backend.routes_extra import extra_bp

# # app = Flask(__name__, template_folder="templates", static_folder="static")
# # app.secret_key = os.environ.get("SECRET_KEY", "change_this_in_production_xyz")
# # CORS(app)
# # app.register_blueprint(extra_bp)

# # ADMIN_EMAIL    = os.environ.get("ADMIN_EMAIL", "admin@gmail.com")
# # ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "Admin@1234")


# # # ── AUTO OPEN BROWSER ────────────────────────────────────────
# # def open_browser(port):
# #     webbrowser.open(f"http://127.0.0.1:{port}/")


# #     # ── PAGE ROUTES ──────────────────────────────────────────────
# # @app.route("/")
# # def index():
# #     return render_template("index.html")

# # @app.route("/admin")
# # def admin_page():
# #     return render_template("admin.html")

# # @app.route("/teacher")
# # def teacher_page():
# #     return render_template("teacher.html")

# # @app.route("/student")
# # def student_page():
# #     return render_template("student.html")


# # # ── AUTH ─────────────────────────────────────────────────────
# # @app.route("/api/admin/login", methods=["POST"])
# # def admin_login():
# #     d = request.json or {}
# #     if d.get("email") == ADMIN_EMAIL and d.get("password") == ADMIN_PASSWORD:
# #         session["role"] = "admin"
# #         return jsonify({"success": True})
# #     return jsonify({"success": False}), 401


# # @app.route("/api/teacher/login", methods=["POST"])
# # def teacher_login():
# #     d = request.json or {}
# #     try:
# #         profile = verify_teacher_login(d["email"], d["password"])
# #         session["role"] = "teacher"
# #         session["uid"] = profile["uid"]
# #         return jsonify({"success": True, "profile": profile})
# #     except PermissionError as e:
# #         return jsonify({"success": False, "message": str(e)}), 403
# #     except Exception:
# #         return jsonify({"success": False}), 401


# # @app.route("/api/logout", methods=["POST"])
# # def logout():
# #     session.clear()
# #     return jsonify({"success": True})


# # # ── TEACHERS ─────────────────────────────────────────────────
# # @app.route("/api/teachers", methods=["GET"])
# # def list_teachers():
# #     return jsonify(get_all_teachers())

# # @app.route('/api/students', methods=['GET'])
# # def get_students():
# #     students = get_all_students()
# #     return jsonify(students)


# # @app.route("/api/teachers", methods=["POST"])
# # def create_teacher():
# #     d = request.json or {}
# #     try:
# #         teacher = add_teacher(
# #     name=d["name"],
# #     email=d["email"],
# #     password=d["password"],
# #     subject=d.get("subject", "")

# #         )
# #         return jsonify({"success": True, "teacher": teacher})
# #     except Exception as e:
# #         return jsonify({"success": False, "message": str(e)}), 400


# # @app.route("/api/teachers/<uid>", methods=["DELETE"])
# # def remove_teacher(uid):
# #     try:
# #         delete_teacher(uid)
# #         return jsonify({"success": True})
# #     except Exception as e:
# #         return jsonify({"success": False, "message": str(e)}), 400


# #     # ── STUDENTS ─────────────────────────────────────────────────
# # @app.route("/api/students", methods=["GET"])
# # def list_students():
# #     return jsonify(get_all_students())


# # @app.route("/api/students", methods=["POST"])
# # def create_student():
# #     try:
# #         # ✅ Get form data (NOT JSON)
# #         name = request.form.get("name")
# #         email = request.form.get("email")
# #         roll_number = request.form.get("roll_number")

# #         # ✅ Get uploaded file
# #         file = request.files.get("face_image")

# #         if not file:
# #             return jsonify({"success": False, "message": "Face image is required"}), 400

# #         # ✅ Convert to bytes
# #         image_bytes = file.read()
# #         image_filename = file.filename

# #         # ✅ Call your function
# #         student = add_student(
# #             name=name,
# #             email=email,
# #             roll_number=roll_number,
# #             face_encoding=None,  # will be generated later in face_engine
# #             image_bytes=image_bytes,
# #             image_filename=image_filename
# #         )

# #         return jsonify({"success": True, "student": student})

# #     except Exception as e:
# #         return jsonify({"success": False, "message": str(e)}), 400


# # @app.route("/api/students/<uid>", methods=["DELETE"])
# # def remove_student(uid):
# #     try:
# #         delete_student(uid)
# #         return jsonify({"success": True})
# #     except Exception as e:
# #         return jsonify({"success": False, "message": str(e)}), 400


# #     # ── CLASSES ──────────────────────────────────────────────────
# # @app.route("/api/classes", methods=["GET"])
# # def list_classes():
# #     return jsonify(get_all_classes())


# # @app.route("/api/classes", methods=["POST"])
# # def make_class():
# #     d = request.json or {}
# #     try:
# #         cls = create_class(
# #             name=d["name"],
# #             teacher_uid=d["teacher_uid"]
# #         )
# #         return jsonify({"success": True, "class": cls})
# #     except Exception as e:
# #         return jsonify({"success": False, "message": str(e)}), 400
    
# # @app.route('/api/classes/<class_id>', methods=['DELETE'])
# # def delete_class(class_id):
# #     try:
# #         db.collection('classes').document(class_id).delete()
# #         return jsonify({"success": True})
# #     except Exception as e:
# #         return jsonify({"success": False, "message": str(e)})


# #     # ── FACE SCAN ────────────────────────────────────────────────
# # @app.route("/api/attendance/scan", methods=["POST"])
# # def start_scan():

# #     def scan():
# #         run_attendance_scan()

# #     threading.Thread(target=scan, daemon=True).start()
# #     return jsonify({"success": True, "message": "Scan started"})


# # # ── HEALTH ───────────────────────────────────────────────────
# # @app.route("/api/health")
# # def health():
# #     return jsonify({"status": "ok"})

# # @app.route('/uploads/<filename>')
# # def uploaded_file(filename):
# #     return send_from_directory('uploads', filename)


# # # --- MAIN ---
# # # if __name__ == "__main__":
# # #     app.run(debug=True)


# # # ── MAIN ─────────────────────────────────────────────────────
# # if __name__ == "__main__":
# #     port = 5000

# #     print("\n=== FaceAttend Running ===")
# #     print(f"http://127.0.0.1:{port}/\n")

# #     # Auto open browser
# #     threading.Timer(1.5, open_browser, args=(port,)).start()

# #     app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)



# import sys
# import os
# import webbrowser
# import threading

# from flask import Flask, request, jsonify, render_template, session, send_from_directory
# from flask_cors import CORS

# from backend.routes_extra import extra_bp
# from backend.firebase_service import get_all_teachers, get_all_students
# from backend.face_engine import run_attendance_scan

# # Load .env
# try:
#     from dotenv import load_dotenv
#     load_dotenv()
# except ImportError:
#     pass

# app = Flask(__name__, template_folder="templates", static_folder="static")
# app.secret_key = os.environ.get("SECRET_KEY", "change_this_in_production_xyz")

# CORS(app)

# # ✅ REGISTER BLUEPRINT (IMPORTANT)
# app.register_blueprint(extra_bp)

# ADMIN_EMAIL    = os.environ.get("ADMIN_EMAIL", "admin@gmail.com")
# ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "Admin@1234")


# # ── AUTO OPEN BROWSER ──
# def open_browser(port):
#     webbrowser.open(f"http://127.0.0.1:{port}/")


#     # ── PAGE ROUTES ──
# @app.route("/")
# def index():
#     return render_template("index.html")


# @app.route("/admin")
# def admin_page():
#     return render_template("admin.html")


# @app.route("/teacher")
# def teacher_page():
#     return render_template("teacher.html")


# @app.route("/student")
# def student_page():
#     return render_template("student.html")


# # ── AUTH ──
# @app.route("/api/admin/login", methods=["POST"])
# def admin_login():
#     d = request.json or {}
#     if d.get("email") == ADMIN_EMAIL and d.get("password") == ADMIN_PASSWORD:
#         session["role"] = "admin"
#         return jsonify({"success": True})
#     return jsonify({"success": False}), 401


# @app.route("/api/logout", methods=["POST"])
# def logout():
#     session.clear()
#     return jsonify({"success": True})


# # ── FACE SCAN ──
# @app.route("/api/attendance/scan", methods=["POST"])
# def start_scan():

#     def scan():
#         run_attendance_scan()

#     threading.Thread(target=scan, daemon=True).start()
#     return jsonify({"success": True, "message": "Scan started"})


# # ── HEALTH ──
# @app.route("/api/health")
# def health():
#     return jsonify({"status": "ok"})


# # ── FILE SERVE ──
# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory('uploads', filename)


# # ── MAIN ──
# if __name__ == "__main__":
#     port = 5000

#     print("\n=== FaceAttend Running ===")
#     print(f"http://127.0.0.1:{port}/\n")

#     threading.Timer(1.5, open_browser, args=(port,)).start()

#     app.run(host="0.0.0.0", port=port, debug=True, use_reloader=False)


import os
import webbrowser
import threading

from flask import Flask, request, jsonify, render_template, session, send_from_directory
from flask_cors import CORS

from backend.routes_extra import extra_bp
from backend.face_engine import run_attendance_scan
from config.firebase_config import get_firestore
db = get_firestore()

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# ✅ ADD THIS LINE
app.register_blueprint(extra_bp)
# Load env
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.environ.get("SECRET_KEY", "change_this_in_production_xyz")

CORS(app)

# ✅ REGISTER BLUEPRINT (ALL APIs HERE)
app.register_blueprint(extra_bp)

ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@gmail.com")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "Admin@1234")


# ================= UI ROUTES =================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/teacher")
def teacher():
    return render_template("teacher.html")


@app.route("/student")
def student():
    return render_template("student.html")


@app.route("/timetable")
def timetable():
    return render_template("timetable.html")


# ================= AUTH =================

@app.route("/api/admin/login", methods=["POST"])
def admin_login():
    d = request.json or {}

    if d.get("email") == ADMIN_EMAIL and d.get("password") == ADMIN_PASSWORD:
        session["role"] = "admin"
        return jsonify({"success": True})

    return jsonify({"success": False}), 401


@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"success": True})




@app.route("/api/teacher/login", methods=["POST"])
def teacher_login():
    try:
        data = request.json

        email = data.get("email")
        password = data.get("password")

        # 🔍 search teacher in firestore
        users = db.collection("users").where("email", "==", email).stream()

        for user in users:
            user_data = user.to_dict()

            # ✅ check role + password
            if user_data.get("role") == "teacher" and user_data.get("password") == password:
                return jsonify({
            "success": True,
            "profile": user_data
        })

        return jsonify({"success": False, "message": "Invalid credentials"}), 401

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500



# ================= ATTENDANCE =================

@app.route("/api/attendance/scan", methods=["POST"])
def scan():
    def run():
        run_attendance_scan()

    threading.Thread(target=run, daemon=True).start()
    return jsonify({"success": True})


# ================= FILE =================

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory("uploads", filename)


# ================= START =================

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == "__main__":
    print("\n🚀 Server running at http://127.0.0.1:5000\n")

    threading.Timer(1.5, open_browser).start()

    app.run(debug=True, use_reloader=False)