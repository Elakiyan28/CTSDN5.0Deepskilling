from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///course_service.db'
db = SQLAlchemy(app)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    credits = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'code': self.code, 'credits': self.credits}


with app.app_context():
    db.create_all()


@app.route('/api/courses/', methods=['GET'])
def list_courses():
    return jsonify([c.to_dict() for c in Course.query.all()])


@app.route('/api/courses/', methods=['POST'])
def create_course():
    payload = request.get_json()
    course = Course(name=payload['name'], code=payload['code'], credits=payload['credits'])
    db.session.add(course)
    db.session.commit()
    return jsonify(course.to_dict()), 201


@app.route('/api/courses/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    course = Course.query.get(course_id)
    if course is None:
        return jsonify({'error': 'Course not found'}), 404
    return jsonify(course.to_dict())


if __name__ == '__main__':
    app.run(port=5001, debug=True)
