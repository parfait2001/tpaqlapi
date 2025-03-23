from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from routes.auth_routes import auth_bp
from routes.room_routes import room_bp
from routes.class_routes import class_bp
from routes.enhanced_class_routes import enhanced_class_bp
from routes.enhanced_room_routes import enhanced_room_bp
from routes.course_routes import course_bp  # Import des routes des cours
from routes.field_routes import field_bp    # Import des routes des filières
from routes.profile_routes import profile_bp  # Import des routes des profils
from routes.user_profile_routes import user_profile_bp
from routes.course_field_routes import course_field_bp



app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Enregistrement des blueprints
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(room_bp, url_prefix='/api')
app.register_blueprint(class_bp, url_prefix='/api')
app.register_blueprint(enhanced_class_bp, url_prefix='/api')
app.register_blueprint(enhanced_room_bp, url_prefix='/api')
app.register_blueprint(course_bp, url_prefix='/api')  # Enregistrement des cours
app.register_blueprint(field_bp, url_prefix='/api')   # Enregistrement des filières
app.register_blueprint(profile_bp, url_prefix='/api')  # Enregistrement des profils
app.register_blueprint(user_profile_bp, url_prefix='/api')
app.register_blueprint(course_field_bp, url_prefix='/api')


if __name__ == '__main__':
    app.run(debug=True)
