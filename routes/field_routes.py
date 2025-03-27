from flask import Blueprint, request, jsonify
from models.field import Field
from models import db

field_bp = Blueprint('field_bp', __name__)

@field_bp.route('/fields', methods=['GET'])
def get_fields():
    fields = Field.query.all()
    return jsonify([field.to_dict() for field in fields]), 200

@field_bp.route('/fields/<int:field_id>', methods=['GET'])
def get_field(field_id):
    field = Field.query.get_or_404(field_id)
    return jsonify(field.to_dict()), 200

@field_bp.route('/fields', methods=['POST'])
def add_field():
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'message': 'Le nom de la filière est requis'}), 400
    
    # Vérifier l'unicité du nom
    existing_field = Field.query.filter_by(name=data['name']).first()
    if existing_field:
        return jsonify({'message': 'Une filière avec ce nom existe déjà'}), 409
    
    new_field = Field(name=data['name'])
    db.session.add(new_field)
    db.session.commit()
    
    return jsonify({
        'message': 'Filière créée avec succès',
        'field': new_field.to_dict()
    }), 201

@field_bp.route('/fields/<int:field_id>', methods=['PATCH'])
def update_field(field_id):
    field = Field.query.get_or_404(field_id)
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'message': 'Le nom de la filière est requis'}), 400
    
    # Vérifier l'unicité du nom (en excluant la filière actuelle)
    existing_field = Field.query.filter(
        Field.name == data['name'],
        Field.id != field_id
    ).first()
    if existing_field:
        return jsonify({'message': 'Une autre filière avec ce nom existe déjà'}), 409
    
    field.name = data['name']
    db.session.commit()
    
    return jsonify({
        'message': 'Filière mise à jour avec succès',
        'field': field.to_dict()
    }), 200

@field_bp.route('/fields/<int:field_id>', methods=['DELETE'])
def delete_field(field_id):
    field = Field.query.get_or_404(field_id)
    
    # Vérifier si la filière est utilisée dans des relations (ex: ClassDetails)
    # Adaptez cette partie selon votre modèle de données
    if field.class_details:
        return jsonify({
            'message': 'Impossible de supprimer cette filière car elle est utilisée',
            'solution': 'Supprimez d\'abord toutes les affectations liées à cette filière'
        }), 400
    
    db.session.delete(field)
    db.session.commit()
    return jsonify({'message': 'Filière supprimée avec succès'}), 200