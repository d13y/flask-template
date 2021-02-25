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

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    image_file = db.Column(db.String(128), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    email_confirm = db.Column(db.Boolean, nullable=False, default=False)
    date_register = db.Column(db.DateTime, nullable=False)
    date_verify = db.Column(db.DateTime, nullable=True)

    # Email authentication
    def get_emailauth_token(self, expires_seconds=900):
        s = Serializer(current_app.config['SECRET_KEY'], expires_seconds)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_emailauth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    # Password reset
    def get_pwreset_token(self, expires_seconds=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_seconds)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_pwreset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
