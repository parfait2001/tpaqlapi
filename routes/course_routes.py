from flask import Blueprint, request, jsonify
from models.course import Course
from models import db

course_bp = Blueprint('course_bp', __name__)

@course_bp.route('/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([course.to_dict() for course in courses]), 200

@course_bp.route('/courses', methods=['POST'])
def add_course():
    data = request.get_json()
    new_course = Course(name=data['name'])
    db.session.add(new_course)
    db.session.commit()
    return jsonify(new_course.to_dict()), 201

@course_bp.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return jsonify({'message': 'Course deleted'}), 200
