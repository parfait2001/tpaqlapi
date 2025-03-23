from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# models/__init__.py
from .classroom import Classroom
from .room import Room
# models/__init__.py
from .user import User
from .profile import Profile
from .user_profile import UserProfile
# Importez d'autres modèles ici

