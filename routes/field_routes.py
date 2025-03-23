from flask import Blueprint, request, jsonify
from models.field import Field
from models import db

field_bp = Blueprint('field_bp', __name__)

@field_bp.route('/fields', methods=['GET'])
def get_fields():
    fields = Field.query.all()
    return jsonify([field.to_dict() for field in fields]), 200

@field_bp.route('/fields', methods=['POST'])
def add_field():
    data = request.get_json()
    new_field = Field(name=data['name'])
    db.session.add(new_field)
    db.session.commit()
    return jsonify(new_field.to_dict()), 201

@field_bp.route('/fields/<int:field_id>', methods=['DELETE'])
def delete_field(field_id):
    field = Field.query.get_or_404(field_id)
    db.session.delete(field)
    db.session.commit()
    return jsonify({'message': 'Field deleted'}), 200
