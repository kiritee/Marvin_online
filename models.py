from flask_mongoengine import MongoEngine
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

db = MongoEngine()

class User(UserMixin, db.Document):
    username = db.StringField(required=True, unique=True)
    password_hash = db.StringField(required=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Session(db.Document):
    user = db.ReferenceField(User, required=True)
    session_name = db.StringField(required=True)
    timestamp = db.DateTimeField(default=datetime.utcnow)
    messages = db.ListField(db.ReferenceField('Message'))

class Message(db.Document):
    session = db.ReferenceField(Session, required=True)
    user_message = db.StringField(required=True)
    bot_response = db.StringField(required=True)
    timestamp = db.DateTimeField(default=datetime.utcnow)
