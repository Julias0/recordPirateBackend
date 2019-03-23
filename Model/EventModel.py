from Config.db import db


class EventModel(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    user = db.relationship('UserModel', uselist=False, backref='events')

    event = db.Column(db.String(1000))
    createdOn = db.Column(db.String(90))

    def __init__(self, event, createdOn):
        self.event = event
        self.createdOn = createdOn

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
            "id": self.id,
            "event": self.name,
            "createdOn": self.createdOn,
            "user": self.user.get_dict()
        }

    @classmethod
    def get_all_events(cls):
        return cls.query.all()
