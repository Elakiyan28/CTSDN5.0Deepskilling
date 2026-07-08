import requests
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_service.db'
db = SQLAlchemy(app)

COURSE_SERVICE_URL = 'http://127.0.0.1:5001'


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'first_name': self.first_name, 'last_name': self.last_name, 'email': self.email}


class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/api/students/', methods=['GET'])
def list_students():
    return jsonify([s.to_dict() for s in Student.query.all()])


@app.route('/api/students/', methods=['POST'])
def create_student():
    payload = request.get_json()
    student = Student(first_name=payload['first_name'], last_name=payload['last_name'], email=payload['email'])
    db.session.add(student)
    db.session.commit()
    return jsonify(student.to_dict()), 201


# Task 2 step 100-101: enroll a student, verifying the course via Course Service
@app.route('/api/students/<int:student_id>/enroll', methods=['POST'])
def enroll(student_id):
    student = Student.query.get(student_id)
    if student is None:
        return jsonify({'error': 'Student not found'}), 404

    payload = request.get_json()
    course_id = payload.get('course_id')

    try:
        resp = requests.get(f'{COURSE_SERVICE_URL}/api/courses/{course_id}/', timeout=3)
    except requests.ConnectionError:
        return jsonify({'error': 'Course Service is unavailable - cannot verify course'}), 503

    if resp.status_code == 404:
        return jsonify({'error': f'Course {course_id} does not exist'}), 400
    if resp.status_code != 200:
        return jsonify({'error': 'Unexpected error from Course Service'}), 502

    enrollment = Enrollment(student_id=student_id, course_id=course_id)
    db.session.add(enrollment)
    db.session.commit()

    return jsonify({'student_id': student_id, 'course': resp.json()}), 201


if __name__ == '__main__':
    app.run(port=5002, debug=True)
