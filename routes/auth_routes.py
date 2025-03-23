from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import bcrypt
from models import db
from models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    firstname = data.get('firstname')

    if not username or not password or not name or not firstname:
        return jsonify({'message': 'Username, password, name et firstname requis'}), 400

    # Vérifiez si le username existe déjà
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username déjà utilisé'}), 400

    # Hachez le mot de passe
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Créez un nouvel utilisateur
    new_user = User(username=username, password=hashed_password.decode('utf-8'), name=name, firstname=firstname)

    # Ajoutez l'utilisateur à la base de données
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Utilisateur enregistré avec succès'}), 201

# Route de connexion
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        access_token = create_access_token(identity=username)
        return jsonify({'token': access_token}), 200
    else:
        return jsonify({'message': 'Identifiants invalides'}), 401

# Route protégée
@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({'message': f'Bienvenue {current_user}!'}), 200


# Profil utilisateur
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    current_user = get_jwt_identity()
    return jsonify({'user': current_user}), 200