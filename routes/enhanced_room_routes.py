from flask import Blueprint, request, jsonify
from models import db, Room  # Corrigez l'importation de Room
from flask_jwt_extended import jwt_required

enhanced_room_bp = Blueprint("enhanced_room", __name__, url_prefix="/rooms")

@enhanced_room_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def update_room(id):
    data = request.json
    room = Room.query.get(id)

    if not room:
        return jsonify({"message": "Salle non trouvée"}), 404

    if "name" in data:
        room.name = data["name"]

    if "available" in data:
        room.available = data["available"]

    db.session.commit()
    return jsonify({"message": "Salle mise à jour avec succès"}), 200

@enhanced_room_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_room(id):
    room = Room.query.get(id)

    if not room:
        return jsonify({"message": "Salle non trouvée"}), 404

    if room.assigned_class:
        return jsonify({"message": "Impossible de supprimer une salle occupée"}), 400

    db.session.delete(room)
    db.session.commit()
    return jsonify({"message": "Salle supprimée"}), 200
