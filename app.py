import os
from flask import Flask, render_template, request, redirect, session, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from dotenv import load_dotenv

# Load .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev_secret_key')

# SQLite config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ------------------------
# Models
# ------------------------

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100))
    grade = db.Column(db.String(10))

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(50))
    email = db.Column(db.String(100))

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10))
    description = db.Column(db.Text)

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

# ------------------------
# Admin credentials (starter)
# ------------------------
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'password123')

# ------------------------
# Helpers
# ------------------------

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated

# ------------------------
# Public routes
# ------------------------

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/events')
def events_page():
    events = Event.query.order_by(Event.date).all()
    return render_template('events.html', events=events)

@app.route('/announcements')
def announcements_page():
    anns = Announcement.query.order_by(Announcement.created_at.desc()).all()
    return render_template('announcements.html', anns=anns)

@app.route('/teachers')
def teachers_page():
    teachers = Teacher.query.all()
    return render_template('teachers.html', teachers=teachers)

# ------------------------
# Admin routes
# ------------------------

@app.route('/admin', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        return render_template('admin_login.html', error='Invalid credentials')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    students_count = Student.query.count()
    teachers_count = Teacher.query.count()
    events_count = Event.query.count()
    return render_template('admin_dashboard.html', students_count=students_count,
                           teachers_count=teachers_count, events_count=events_count)

@app.route('/admin/add_event', methods=['GET','POST'])
@admin_required
def add_event():
    if request.method == 'POST':
        title = request.form['title']
        date = request.form.get('date')
        description = request.form['description']
        event = Event(title=title, date=date, description=description)
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('events_page'))
    return render_template('add_event.html')

@app.route('/admin/add_announcement', methods=['GET','POST'])
@admin_required
def add_announcement():
    if request.method == 'POST':
        message = request.form['message']
        ann = Announcement(message=message)
        db.session.add(ann)
        db.session.commit()
        return redirect(url_for('announcements_page'))
    return render_template('add_announcement.html')

# ------------------------
# Student auth & dashboard
# ------------------------

@app.route('/student/login', methods=['GET','POST'])
def student_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        student = Student.query.filter_by(username=username, password=password).first()
        if student:
            session['student_id'] = student.id
            session['student_username'] = student.username
            session['student_name'] = student.name
            session['student_grade'] = student.grade
            return redirect(url_for('student_dashboard'))
        return render_template('student_login.html', error='Invalid login')
    return render_template('student_login.html')

@app.route('/student/logout')
def student_logout():
    session.clear()
    return redirect(url_for('student_login'))

@app.route('/student/dashboard')
def student_dashboard():
    if not session.get('student_id'):
        return redirect(url_for('student_login'))
    return render_template('student_dashboard.html', student=session)

# ------------------------
# API endpoints
# ------------------------

@app.route('/api/events')
def api_events():
    events = Event.query.order_by(Event.date).all()
    events_list = [{'id': e.id, 'title': e.title, 'date': e.date, 'description': e.description} for e in events]
    return jsonify(events_list)

@app.route('/api/announcements')
def api_announcements():
    anns = Announcement.query.order_by(Announcement.created_at.desc()).all()
    anns_list = [{'id': a.id, 'message': a.message, 'created_at': str(a.created_at)} for a in anns]
    return jsonify(anns_list)

# ------------------------
# Error handlers
# ------------------------

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

# ------------------------
# Run
# ------------------------

if __name__ == '__main__':
    with app.app_context():  # <-- add this
        db.create_all()      # Creates tables if they don't exist
    app.run(debug=True)

