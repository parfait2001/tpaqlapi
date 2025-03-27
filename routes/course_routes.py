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
    
    if not data or 'name' not in data:
        return jsonify({'message': 'Name is required'}), 400
    
    # Vérifier l'unicité du nom
    existing_course = Course.query.filter_by(name=data['name']).first()
    if existing_course:
        return jsonify({'message': 'A course with this name already exists'}), 409
    
    new_course = Course(name=data['name'])
    db.session.add(new_course)
    db.session.commit()
    return jsonify(new_course.to_dict()), 201

@course_bp.route('/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    course = Course.query.get_or_404(course_id)
    return jsonify(course.to_dict()), 200

@course_bp.route('/courses/<int:course_id>', methods=['PATCH'])
def update_course(course_id):
    course = Course.query.get_or_404(course_id)
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'message': 'Name is required'}), 400
    
    # Vérifier l'unicité du nom (en excluant le cours actuel)
    existing_course = Course.query.filter(
        Course.name == data['name'],
        Course.id != course_id
    ).first()
    if existing_course:
        return jsonify({'message': 'Another course with this name already exists'}), 409
    
    course.name = data['name']
    db.session.commit()
    return jsonify(course.to_dict()), 200

@course_bp.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return jsonify({'message': 'Course deleted successfully'}), 200