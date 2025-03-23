from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db
from models.room import Room

room_bp = Blueprint('room', __name__)

# Ajouter une salle
@room_bp.route('/rooms', methods=['POST'])
@jwt_required()
def add_room():
    data = request.json
    name = data.get('name')

    if not name:
        return jsonify({'message': 'Nom de la salle requis'}), 400

    new_room = Room(name=name)
    db.session.add(new_room)
    db.session.commit()

    return jsonify({'message': 'Salle créée avec succès'}), 201

# Consulter les salles disponibles
@room_bp.route('/rooms', methods=['GET'])
@jwt_required()
def get_rooms():
    available = request.args.get('available')

    if available is not None:
        rooms = Room.query.filter_by(available=bool(int(available))).all()
    else:
        rooms = Room.query.all()

    return jsonify([{'id': room.id, 'name': room.name, 'available': room.available} for room in rooms]), 200