from flask import Blueprint, request, jsonify
from models import db, Classroom, Room  # Utilisez Classroom ici
from flask_jwt_extended import jwt_required

enhanced_class_bp = Blueprint("enhanced_class", __name__, url_prefix="/classes")

@enhanced_class_bp.route("/", methods=["GET"])
@jwt_required()
def list_classes():
    classes = Classroom.query.all()  # Utilisez Classroom ici
    return jsonify([cls.to_dict() for cls in classes]), 200

@enhanced_class_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def update_class(id):
    data = request.json
    classroom = Classroom.query.get(id)  # Utilisez Classroom ici

    if not classroom:
        return jsonify({"message": "Classe non trouvée"}), 404

    if "name" in data:
        classroom.name = data["name"]

    if "available" in data:
        classroom.available = data["available"]

    db.session.commit()
    return jsonify({"message": "Classe mise à jour avec succès"}), 200

@enhanced_class_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_class(id):
    classroom = Classroom.query.get(id)  # Utilisez Classroom ici

    if not classroom:
        return jsonify({"message": "Classe non trouvée"}), 404

    if not classroom.available:
        return jsonify({"message": "Impossible de supprimer une classe occupée"}), 400

    db.session.delete(classroom)
    db.session.commit()
    return jsonify({"message": "Classe supprimée"}), 200
