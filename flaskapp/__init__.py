from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskapp.config import Config

# Configuration extensions
db = SQLAlchemy()  # initialise database
bcrypt = Bcrypt()  # encrypt passwords
mail = Mail()  # enable emails from server
login_manager = LoginManager()  # handle login functionality

# Additional configuration parameters (for login)
login_manager.login_view = 'users.login'  # for pages requiring login, re-routes to 'login' page if required
login_manager.login_message_category = 'info'  # to match bootstrap css class for info messages


# Configuration setup
def create_app(config_class=Config):

    app = Flask(__name__)  # create an app instance
    app.config.from_object(Config)  # import Config class details

    # Link extensions to app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # Import blueprints
    from flaskapp.users.routes import users  # inserted here to prevent circular reference
    from flaskapp.main.routes import main  # inserted here to prevent circular reference
    app.register_blueprint(users)  # register user directory functionality
    app.register_blueprint(main)  # register main directory functionality

    return app
