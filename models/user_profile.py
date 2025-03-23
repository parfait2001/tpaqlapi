from models import db

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('user_profiles', cascade="all, delete-orphan"))
    profile = db.relationship('Profile', backref=db.backref('profile_users', cascade="all, delete-orphan"))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'profile_id': self.profile_id
        }
