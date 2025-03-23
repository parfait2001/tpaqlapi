from models import db

class Field(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    # Relation avec Course (Many-to-Many)
    courses = db.relationship('Course', secondary='course_field', back_populates='fields')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
