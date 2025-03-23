from models import db

# Table d'association Many-to-Many entre Course et Field
course_field = db.Table(
    'course_field',
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True),
    db.Column('field_id', db.Integer, db.ForeignKey('field.id'), primary_key=True)
)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    # Relation avec Field (Many-to-Many)
    fields = db.relationship('Field', secondary=course_field, back_populates='courses')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
