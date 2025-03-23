from flask import Blueprint, request, jsonify
from models import db
from models.course import Course
from models.field import Field

course_field_bp = Blueprint('course_field', __name__)

@course_field_bp.route('/assign-course-field', methods=['POST'])
def assign_course_field():
    data = request.get_json()
    course_id = data.get('course_id')
    field_id = data.get('field_id')

    course = Course.query.get(course_id)
    field = Field.query.get(field_id)

    if not course or not field:
        return jsonify({"error": "Cours ou filière introuvable"}), 404

    # Ajouter la relation Many-to-Many
    course.fields.append(field)
    db.session.commit()

    return jsonify({"message": "Cours assigné à la filière avec succès"}), 201
