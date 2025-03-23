from flask import Blueprint, request, jsonify
from models import db
from models.user_profile import UserProfile
from models.user import User
from models.profile import Profile

user_profile_bp = Blueprint('user_profile', __name__)

@user_profile_bp.route('/assign-profile', methods=['POST'])
def assign_profile():
    data = request.get_json()
    user_id = data.get('user_id')
    profile_id = data.get('profile_id')

    user = User.query.get(user_id)
    profile = Profile.query.get(profile_id)

    if not user or not profile:
        return jsonify({"error": "Utilisateur ou profil introuvable"}), 404

    user_profile = UserProfile(user_id=user_id, profile_id=profile_id)
    db.session.add(user_profile)
    db.session.commit()

    return jsonify({"message": "Profil assigné avec succès", "data": user_profile.to_dict()}), 201
