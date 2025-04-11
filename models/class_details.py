from models import db
from sqlalchemy.sql import func

class ClassDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=True)
    field_id = db.Column(db.Integer, db.ForeignKey('field.id'), nullable=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classroom.id'), nullable=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=True)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)

    course = db.relationship('Course', backref=db.backref('class_details', lazy=True))
    field = db.relationship('Field', backref=db.backref('class_details', lazy=True))
    classroom = db.relationship('Classroom', backref=db.backref('class_details', lazy=True))
    room = db.relationship('Room', backref=db.backref('class_details', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'field_id': self.field_id,
            'class_id': self.class_id,
            'room_id': self.room_id,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat()
        }
