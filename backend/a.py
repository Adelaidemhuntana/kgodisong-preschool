import os
import hashlib
import json
import requests
import random
import string
from datetime import datetime
from functools import wraps
from flask import (
    Flask, request, jsonify, render_template,
    redirect, url_for, session, send_from_directory
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from reference import generate_ai_reference, generate_ai_checkup_reference
from app.llama_service import ask_health_assistant, ask_emergency

# -----------------------------
# Flask Setup
# -----------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))

app = Flask(
    __name__,
    template_folder=FRONTEND_DIR,
    static_folder=os.path.join(FRONTEND_DIR, "static"),
    static_url_path="/static"
)

app.secret_key = "supersecretkey"

DB_PATH = os.path.join(BASE_DIR, "healthhub.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# -----------------------------
# Ambulance JSON Storage
# -----------------------------
AMBULANCE_JSON = os.path.join(BASE_DIR, "ambulance_requests.json")
if not os.path.exists(AMBULANCE_JSON):
    with open(AMBULANCE_JSON, "w") as f:
        json.dump([], f)

def save_ambulance_request(data):
    try:
        with open(AMBULANCE_JSON, "r") as f:
            existing = json.load(f)
    except:
        existing = []
    existing.append(data)
    with open(AMBULANCE_JSON, "w") as f:
        json.dump(existing, f, indent=4)

# -----------------------------
# Utilities
# -----------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(raw, hashed):
    return hash_password(raw) == hashed

def _get_field(name):
    if request.form and name in request.form:
        return request.form.get(name)
    if request.is_json:
        data = request.get_json(silent=True) or {}
        if name in data:
            return data.get(name)
    if name in request.args:
        return request.args.get(name)
    return None

def require_login():
    return "username" in session

# -----------------------------
# Decorators
# -----------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not require_login():
            return redirect(url_for("login_page"))
        return f(*args, **kwargs)
    return decorated_function

def api_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not require_login():
            return jsonify({"status": "error", "message": "Login required"}), 401
        return f(*args, **kwargs)
    return decorated_function

# -----------------------------
# Models
# -----------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    grade = db.Column(db.String(80))

class AmbulanceBooking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    child_name = db.Column(db.String(120), nullable=False)
    class_name = db.Column(db.String(80), nullable=False)
    emergency_type = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    reference_number = db.Column(db.String(50), unique=True, nullable=False)

class SickLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    child_name = db.Column(db.String(120), nullable=False)
    grade = db.Column(db.String(80), nullable=False)
    symptoms = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(20), nullable=False)

class CheckupBooking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    child_name = db.Column(db.String(120), nullable=False)
    parent_email = db.Column(db.String(120), nullable=False)
    check_type = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    reference_number = db.Column(db.String(50), unique=True, nullable=False)

class VaccineBooking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    child_name = db.Column(db.String(120), nullable=False)
    vaccine_type = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    reference = db.Column(db.String(50), unique=True, nullable=False)

# -----------------------------
# User Management
# -----------------------------
def create_user(username, password, role):
    username = (username or "").strip()
    password = (password or "").strip()
    if User.query.filter_by(username=username).first():
        return False
    user = User(username=username, password=hash_password(password), role=role)
    db.session.add(user)
    db.session.commit()
    return True

# -----------------------------
# Authentication Routes
# -----------------------------
@app.route("/api/signup", methods=["POST"])
def signup():
    username = _get_field("username")
    password = _get_field("password") or "123456"
    role = _get_field("role") or "parent"
    if not username:
        return ("Missing username", 400)
    if not User.query.filter_by(username=username).first():
        create_user(username, password, role)
    session["username"] = username
    session["role"] = role
    return redirect(url_for("dashboard") if role.lower() == "parent" else url_for("admin_dashboard"))

@app.route("/api/login", methods=["POST"])
def login():
    username = _get_field("username")
    role = _get_field("role") or "parent"
    if not username:
        return ("Missing username", 400)
    user = User.query.filter_by(username=username).first()
    if not user:
        create_user(username, "123456", role)
        user = User.query.filter_by(username=username).first()
    session["username"] = user.username
    session["role"] = user.role
    if user.role.lower() in ["admin", "teacher"]:
        return redirect(url_for("admin_dashboard"))
    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# -----------------------------
# Session Check API
# -----------------------------
@app.route("/api/check-session")
def check_session():
    return jsonify({"logged_in": require_login()})

# -----------------------------
# Dashboards
# -----------------------------
@app.route("/dashboard")
@login_required
def dashboard():
    if session.get("role").lower() in ["admin", "teacher"]:
        return redirect(url_for("admin_dashboard"))
    return render_template("hub-dashboard.html")

@app.route("/admin-dashboard")
@login_required
def admin_dashboard():
    if session.get("role").lower() not in ["admin", "teacher"]:
        return redirect(url_for("login_page"))
    return render_template("hub-dashboard.html")

# -----------------------------
# Pages
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/<path:resource>")
def serve_resource(resource):
    safe_path = os.path.normpath(os.path.join(FRONTEND_DIR, resource))
    if not safe_path.startswith(FRONTEND_DIR):
        return ("Invalid path", 400)
    if os.path.exists(safe_path) and os.path.isfile(safe_path):
        rel = os.path.relpath(safe_path, FRONTEND_DIR)
        return send_from_directory(FRONTEND_DIR, rel)
    try:
        return render_template(resource)
    except Exception:
        return ("Not Found", 404)


# -----------------------------
# Protected Health Pages
# -----------------------------
@app.route("/health/immunization-booking")
@login_required
def immunization_page():
    return render_template("Immunization-Booking.html")

@app.route("/health/sick-absenteeism")
@login_required
def sick_page():
    return render_template("sick-log.html")

@app.route("/health/eye-dental-bookings")
@login_required
def eye_dental_page():
    return render_template("eye-dental-booking.html")

@app.route("/health/school-pharmacy")
@login_required
def pharmacy_page():
    return render_template("pharmacy.html")

@app.route("/health/ambulance-request")
@login_required
def ambulance_page():
    return render_template("ambulance-request.html")

@app.route("/health/ai-assistant")
@login_required
def ai_page():
    return render_template("chatbot.html")

# -----------------------------
# Form Handlers (Protected APIs)
# -----------------------------
@app.route("/api/sick-log", methods=["POST"])
@api_login_required
def sick_log_form():
    data = request.form
    entry = SickLog(
        child_name=data["child_name"],
        grade=data["grade"],
        symptoms=data["symptoms"],
        description=data["description"],
        date=data["date"]
    )
    db.session.add(entry)
    db.session.commit()
    return jsonify({"status": "success"})

@app.route("/api/checkup-booking", methods=["POST"])
@api_login_required
def checkup_form():
    data = request.form
    reference_number = generate_ai_checkup_reference(data["check_type"])
    entry = CheckupBooking(
        child_name=data["child_name"],
        parent_email=data["parent_email"],
        check_type=data["check_type"],
        date=data["date"],
        reference_number=reference_number
    )
    db.session.add(entry)
    db.session.commit()
    return jsonify({
        "status": "success",
        "reference": reference_number,
        "check_type": data["check_type"],
        "parent_email": data["parent_email"]
    }), 200

@app.route("/api/vaccine-booking", methods=["POST"])
@api_login_required
def vaccine_form():
    data = request.form
    reference_number = generate_ai_reference(data["vaccine_type"])
    entry = VaccineBooking(
        child_name=data["child_name"],
        vaccine_type=data["vaccine_type"],
        date=data["date"],
        reference=reference_number
    )
    db.session.add(entry)
    db.session.commit()
    return jsonify({"status": "success", "reference": reference_number}), 200

# -----------------------------
# Ambulance Booking with AI Assistance
# -----------------------------
@app.route("/api/ambulance-booking", methods=["POST"])
@api_login_required
def ambulance_booking():
    data = request.form
    child_name = data["child_name"]
    emergency_type = data["emergency_type"]

    # Generate unique reference
    ref = "AMB-" + datetime.now().strftime("%Y%m%d") + "-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    hospitals = ["Mediclinic", "Netcare", "Life Healthcare", "Charlotte Maxeke Hospital"]
    selected_hospital = random.choice(hospitals)

    entry = AmbulanceBooking(
        child_name=child_name,
        class_name=data["class_name"],
        emergency_type=emergency_type,
        description=data["description"],
        reference_number=ref
    )
    db.session.add(entry)
    db.session.commit()
    save_ambulance_request({
        "reference_number": ref,
        "child_name": child_name,
        "class_name": data["class_name"],
        "emergency_type": emergency_type,
        "description": data["description"],
        "hospital": selected_hospital,
        "timestamp": datetime.now().isoformat()
    })

    eta_minutes = random.randint(5, 15)

    # Fetch previous illness records
    previous_records = SickLog.query.filter_by(child_name=child_name).all()
    previous_illnesses = [
        {"date": r.date, "symptoms": r.symptoms, "description": r.description} for r in previous_records
    ]

    suggested_actions = [
        "Keep the child calm and comfortable.",
        "Check the child's breathing and pulse if necessary.",
        "Prepare any relevant medical information for the ambulance staff.",
        "Clear a safe path for the ambulance to reach you quickly.",
        "Stay on the phone with emergency services if advised."
    ]

    # AI guidance based on previous illnesses
    ai_suggestions = []
    if previous_illnesses:
        ai_suggestions.append(
            f"Previous illnesses for {child_name}: " +
            ", ".join([r["symptoms"] for r in previous_illnesses[-3:]]) +
            ". Monitor for similar symptoms."
        )

    # Emergency-specific guidance
    emergency_guidance = []
    if "fever" in emergency_type.lower():
        emergency_guidance = [
            "Monitor the child's temperature regularly.",
            "Keep the child hydrated.",
            "Do not give any medication unless prescribed by a doctor.",
            "Remove excess clothing and keep the room cool."
        ]
    elif "injury" in emergency_type.lower() or "cut" in emergency_type.lower():
        emergency_guidance = [
            "Apply gentle pressure to stop any bleeding.",
            "Keep the injured area elevated if possible.",
            "Do not try to move the child if there is suspected fracture.",
            "Keep the child calm and still."
        ]
    elif "allergic" in emergency_type.lower():
        emergency_guidance = [
            "Check if the child has an epinephrine auto-injector and use if prescribed.",
            "Remove any allergen from immediate environment.",
            "Monitor breathing and pulse continuously.",
            "Keep the child calm and lying down."
        ]
    elif "breathing" in emergency_type.lower() or "asthma" in emergency_type.lower():
        emergency_guidance = [
            "Help the child sit upright.",
            "Give prescribed inhaler if available.",
            "Keep airways clear and calm the child.",
            "Monitor breathing closely until help arrives."
        ]
    else:
        emergency_guidance = ["Follow general first-aid measures and keep the child comfortable."]

    ai_suggestions.extend(emergency_guidance)

    return jsonify({
        "status": "success",
        "reference": ref,
        "hospital": selected_hospital,
        "eta_minutes": eta_minutes,
        "message": f"Ambulance request sent to {selected_hospital}. Help is on the way! ETA: {eta_minutes} minutes.",
        "suggested_actions": suggested_actions,
        "ai_suggestions": ai_suggestions,
        "previous_illnesses": previous_illnesses
    }), 200

# -----------------------------
# AI Health Assistant Endpoint
# -----------------------------
@app.route("/api/ask-ai", methods=["POST"])
@api_login_required
def ask_ai():
    """
    Handles chatbot requests using the local Llama module.
    Optional: child_name and age for personalized guidance.
    """
    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()
    child_name = data.get("child_name", "").strip()
    age = data.get("age")  # Optional: pass age in years

    if not question:
        return jsonify({"answer": "❗ Please ask a valid question."})

    # Optional: fetch past sickness history
    sickness_history = []
    if child_name:
        logs = SickLog.query.filter_by(child_name=child_name).all()
        for log in logs:
            sickness_history.append(f"{log.date}: {log.symptoms} - {log.description}")

    # Prepare prompt category
    category = data.get("category", "General")

    try:
        # If age is provided, use integer; otherwise default to 3 years
        age_int = int(age) if age else 3

        # Call your Llama wrapper
        answer = ask_health_assistant(question=question, category=category, age=age_int)

        # Include sickness history in response if available
        if sickness_history:
            history_text = "\n".join(sickness_history)
            answer = f"{answer}\n\nChild sickness history:\n{history_text}"

    except Exception as e:
        print("Llama API error:", e)
        answer = "❗ Sorry, the AI service is temporarily unavailable."

    return jsonify({"answer": answer})

# -----------------------------
# Admin Health Rules Management
# -----------------------------

@app.route("/admin/health-rules", methods=["POST"])
def update_rules():
   if session.get("role") != "admin":
       return ("Forbidden", 403)
   new_rules = request.get_json(silent=True) or []
   RULES_JSON = os.path.join(BASE_DIR, "health_rules.json")
   with open(RULES_JSON, "w") as f:
       json.dump(new_rules, f, indent=4)
   return jsonify({"status": "success"})


# -----------------------------
# Demo Data
# -----------------------------
def create_demo_data():
    if not User.query.filter_by(username="parent@kgodisong.com").first():
        create_user("parent@kgodisong.com", "123456", "parent")
    if not User.query.filter_by(username="teacher@kgodisong.com").first():
        create_user("teacher@kgodisong.com", "123456", "teacher")
    if not User.query.filter_by(username="admin@kgodisong.com").first():
        create_user("admin@kgodisong.com", "123456", "admin")
    if not Student.query.filter_by(name="John Doe").first():
        db.session.add(Student(name="John Doe", grade="Grade 1"))
    if not Student.query.filter_by(name="Jane Smith").first():
        db.session.add(Student(name="Jane Smith", grade="Grade 2"))
    db.session.commit()

# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_demo_data()
    print("Kgodisong Health Hub Running: http://127.0.0.1:5000/ 🚀")
    app.run(host="0.0.0.0", port=5000, debug=True)
