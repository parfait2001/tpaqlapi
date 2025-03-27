from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db
from models.room import Room

room_bp = Blueprint('room', __name__)

@room_bp.route('/rooms', methods=['POST'])
@jwt_required()
def add_room():
    data = request.json
    name = data.get('name')

    if not name:
        return jsonify({'message': 'Nom de la salle requis'}), 400

    # Vérifier si une salle avec ce nom existe déjà
    existing_room = Room.query.filter_by(name=name).first()
    if existing_room:
        return jsonify({'message': 'Une salle avec ce nom existe déjà'}), 409

    new_room = Room(name=name)
    db.session.add(new_room)
    db.session.commit()

    return jsonify({
        'message': 'Salle créée avec succès',
        'room': {
            'id': new_room.id,
            'name': new_room.name,
            'available': new_room.available
        }
    }), 201

@room_bp.route('/rooms', methods=['GET'])
@jwt_required()
def get_rooms():
    available = request.args.get('available')
    
    query = Room.query
    
    if available is not None:
        try:
            available_bool = bool(int(available))
            query = query.filter_by(available=available_bool)
        except ValueError:
            return jsonify({'message': 'Paramètre "available" doit être 0 ou 1'}), 400

    rooms = query.all()
    return jsonify([{
        'id': room.id,
        'name': room.name,
        'available': room.available
    } for room in rooms]), 200

@room_bp.route('/rooms/<int:room_id>', methods=['GET'])
@jwt_required()
def get_room(room_id):
    room = Room.query.get_or_404(room_id)
    return jsonify({
        'id': room.id,
        'name': room.name,
        'available': room.available
    }), 200

@room_bp.route('/rooms/<int:room_id>', methods=['PATCH'])
@jwt_required()
def update_room(room_id):
    room = Room.query.get_or_404(room_id)
    data = request.json
    name = data.get('name')
    available = data.get('available')

    if not any([name, available]):
        return jsonify({'message': 'Aucune donnée à mettre à jour'}), 400

    if name is not None:
        # Vérifier l'unicité du nom (en excluant la salle actuelle)
        existing_room = Room.query.filter(
            Room.name == name,
            Room.id != room_id
        ).first()
        if existing_room:
            return jsonify({'message': 'Une autre salle avec ce nom existe déjà'}), 409
        room.name = name

    if available is not None:
        try:
            room.available = bool(available)
        except ValueError:
            return jsonify({'message': 'Le champ "available" doit être un booléen'}), 400

    db.session.commit()
    return jsonify({
        'message': 'Salle mise à jour avec succès',
        'room': {
            'id': room.id,
            'name': room.name,
            'available': room.available
        }
    }), 200

@room_bp.route('/rooms/<int:room_id>', methods=['DELETE'])
@jwt_required()
def delete_room(room_id):
    room = Room.query.get_or_404(room_id)
    
    # Vérifier si la salle est actuellement utilisée
    if not room.available:
        return jsonify({
            'message': 'Impossible de supprimer cette salle car elle est actuellement utilisée',
            'solution': 'Libérez d\'abord la salle avant de la supprimer'
        }), 400

    db.session.delete(room)
    db.session.commit()
    return jsonify({'message': 'Salle supprimée avec succès'}), 200