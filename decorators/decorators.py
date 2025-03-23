# decorators.py
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from models import User

def role_required(role_name):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)

            # Vérifiez si l'utilisateur a le rôle requis
            has_role = any(up.profil.name == role_name for up in user.profiles)
            if not has_role:
                return jsonify({'message': 'Accès non autorisé'}), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator
