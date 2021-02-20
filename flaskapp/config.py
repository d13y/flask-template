import os


class Config:

    # General configuration
    SECRET_KEY = os.environ.get('EV_SECRET_KEY')  # key required for accounts
    SQLALCHEMY_DATABASE_URI = os.environ.get('EV_SQL_DATABASE')  # database location

    # Mail configuration
    MAIL_SERVER = 'smtp.googlemail.com'  # using gmail
    MAIL_PORT = '587'  # req port info
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EV_EMAIL_USER')  # gmail account
    MAIL_PASSWORD = os.environ.get('EV_EMAIL_PASS')  # gmail password
