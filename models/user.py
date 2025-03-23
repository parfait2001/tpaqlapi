from models import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)  # Ajout du champ name
    firstname = db.Column(db.String(100), nullable=False)  # Ajout du champ firstname
