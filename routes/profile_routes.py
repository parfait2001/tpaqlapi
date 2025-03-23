from flask import Blueprint, request, jsonify
from models.profile import Profile
from models import db

profile_bp = Blueprint('profile_bp', __name__)

@profile_bp.route('/profiles', methods=['GET'])
def get_profiles():
    profiles = Profile.query.all()
    return jsonify([profile.to_dict() for profile in profiles]), 200

@profile_bp.route('/profiles', methods=['POST'])
def add_profile():
    data = request.get_json()
    new_profile = Profile(name=data['name'])
    db.session.add(new_profile)
    db.session.commit()
    return jsonify(new_profile.to_dict()), 201

@profile_bp.route('/profiles/<int:profile_id>', methods=['DELETE'])
def delete_profile(profile_id):
    profile = Profile.query.get_or_404(profile_id)
    db.session.delete(profile)
    db.session.commit()
    return jsonify({'message': 'Profile deleted'}), 200
