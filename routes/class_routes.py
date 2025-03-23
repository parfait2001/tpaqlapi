from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db
from models.classroom import Classroom
from models.room import Room
from models.course import Course
from models.field import Field
from models.class_details import ClassDetails
from decorators.decorators import role_required  # Importez le décorateur ici

class_bp = Blueprint('class', __name__)

# Créer une classe
@class_bp.route('/classes', methods=['POST'])
@jwt_required()
def create_class():
    data = request.json
    name = data.get('name')

    if not name:
        return jsonify({'message': 'Nom de la classe requis'}), 400

    new_class = Classroom(name=name)
    db.session.add(new_class)
    db.session.commit()

    return jsonify({'message': 'Classe créée avec succès'}), 201

@class_bp.route('/classes', methods=['GET'])
def get_class():
    classrooms = Classroom.query.all()
    return jsonify([classroom.to_dict() for classroom in classrooms]), 200

@class_bp.route('/classes/<int:class_id>', methods=['PATCH'])
@jwt_required()
#@role_required('gestionnaire')
def update_class(class_id):
    data = request.json
    name = data.get('name')

    classroom = Classroom.query.get(class_id)
    if not classroom:
        return jsonify({'message': 'Classe non trouvée'}), 404

    if name:
        classroom.name = name

    db.session.commit()
    return jsonify({'message': 'Classe mise à jour avec succès'}), 200

@class_bp.route('/classes/<int:class_id>', methods=['DELETE'])
@jwt_required()
#@role_required('admin')
def delete_class(class_id):
    classroom = Classroom.query.get(class_id)
    if not classroom:
        return jsonify({'message': 'Classe non trouvée'}), 404

    db.session.delete(classroom)
    db.session.commit()
    return jsonify({'message': 'Classe supprimée avec succès'}), 200


# Assigner une salle à une classe
@class_bp.route('/assign-room', methods=['POST'])
@jwt_required()
def assign_room():
    data = request.json
    class_id = data.get('class_id')
    room_id = data.get('room_id')
    course_id = data.get('course_id')
    field_id = data.get('field_id')
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    if not all([class_id, room_id, course_id, field_id, start_time, end_time]):
        return jsonify({'message': 'Données manquantes dans la requête'}), 400

    classroom = Classroom.query.get(class_id)
    room = Room.query.get(room_id)
    course = Course.query.get(course_id)
    field = Field.query.get(field_id)

    if not classroom or not room or not course or not field:
        return jsonify({'message': 'Classe, salle, cours ou filière non trouvée'}), 404

    if not room.available:
        return jsonify({'message': 'Salle non disponible'}), 400

    classroom.room_id = room_id
    room.available = False

    class_details = ClassDetails(
        course_id=course_id,
        field_id=field_id,
        class_id=class_id,
        room_id=room_id,
        start_time=start_time,
        end_time=end_time
    )
    db.session.add(class_details)
    db.session.commit()

    return jsonify({'message': 'Salle assignée à la classe', 'details': class_details.to_dict()}), 200

@class_bp.route('/dessign-room', methods=['POST'])
@jwt_required()
#@role_required('gestionnaire')
def dessign_room():
    data = request.json
    class_id = data.get('class_id')
    room_id = data.get('room_id')

    if not class_id or not room_id:
        return jsonify({'message': 'Données manquantes dans la requête'}), 400

    classroom = Classroom.query.get(class_id)
    room = Room.query.get(room_id)

    if not classroom or not room:
        return jsonify({'message': 'Classe ou salle non trouvée'}), 404

    if classroom.room_id != room_id:
        return jsonify({'message': 'Cette salle n\'est pas assignée à cette classe'}), 400

    classroom.room_id = None
    room.available = True

    class_details = ClassDetails.query.filter_by(class_id=class_id, room_id=room_id).first()
    if class_details:
        db.session.delete(class_details)

    db.session.commit()
    return jsonify({'message': 'Salle désassignée avec succès'}), 200
