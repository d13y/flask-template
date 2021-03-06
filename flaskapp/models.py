from flask import current_app
from flaskapp import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


# Handle login for active user sessions
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Setup user database
# noinspection PyBroadException
class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)  # unique id
    username = db.Column(db.String(12), unique=True, nullable=False)  # unique username
    email = db.Column(db.String(128), unique=True, nullable=False)  # unique email
    image_file = db.Column(db.String(128), nullable=False, default='default.jpg')  # profile pic
    password = db.Column(db.String(60), nullable=False)  # password (hashed)
    confirm_account = db.Column(db.Boolean, nullable=False, default=False)  # has account been verified?
    date_register = db.Column(db.DateTime, nullable=False)  # date/time when initial registry
    date_verify = db.Column(db.DateTime, nullable=True)  # date/time when account verified
    temp_email = db.Column(db.String(128), unique=True, nullable=True)  # to store new email until verified (if changed)

    # Email authentication
    def get_auth_token_email(self, expires_seconds=900):  # create token, valid for 15 mins
        s = Serializer(current_app.config['SECRET_KEY'], expires_seconds)
        return s.dumps({'user_id': self.id}).decode('utf-8')  # link key to user

    @staticmethod
    def verify_auth_token_email(token):  # verify token, if valid
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']  # check if token is valid
        except:
            return None
        return User.query.get(user_id)

    # Password reset
    def get_reset_token_pw(self, expires_seconds=3600):  # create token, valid for 60 mins
        s = Serializer(current_app.config['SECRET_KEY'], expires_seconds)
        return s.dumps({'user_id': self.id}).decode('utf-8')  # link key to user

    @staticmethod
    def verify_reset_token_pw(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']  # check if token is valid
        except:
            return None
        return User.query.get(user_id)

    # return values usable elsewhere
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
