from datetime import datetime
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskapp.models import User


# Registration
class RegistrationForm(FlaskForm):

    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=12)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirmpassword = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # To validate username is unique
    def validate_username(self, username):
        olduser = User.query.filter(User.username.ilike(username.data)).first()  # search db for existing username
        if olduser:  # if username found in existing database
            timediff = datetime.now() - olduser.date_register  # time since username registered/created
            if olduser.confirm_account or timediff.seconds < 900:  # check if user verified, or token still valid
                raise ValidationError('Username already taken.')

    # To validate username is unique
    def validate_email(self, email):
        oldemail = User.query.filter(User.email.ilike(email.data)).first()  # search db for existing email
        if oldemail:  # if email found in existing database
            timediff = datetime.now() - oldemail.date_register  # time since email registered
            if oldemail.confirm_account or timediff.seconds < 900:  # check if email verified, or token still valid
                raise ValidationError('Email already taken.')


# Login
class LoginForm(FlaskForm):

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


# Update account
class UpdateAccountForm(FlaskForm):

    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=12)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])  # only allowed extensions
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:  # check username isn't the same as current username
            olduser = User.query.filter(User.username.ilike(username.data)).first()  # search db for existing username
            if olduser:  # if username found in existing database
                timediff = datetime.now() - olduser.date_register  # time since username registered/created
                if olduser.confirm_account or timediff.seconds < 900:  # check if user verified, or token still valid
                    raise ValidationError('Username already taken.')

    def validate_email(self, email):
        if email.data != current_user.email:  # check email isn't the same as current email
            oldemail = User.query.filter(User.email.ilike(email.data)).first()  # search db for existing email
            if oldemail:  # if email found in existing database
                timediff = datetime.now() - oldemail.date_register  # time since email registered
                if oldemail.confirm_account or timediff.seconds < 900:  # check if email verified, or token still valid
                    raise ValidationError('Email already taken.')


# Email reset confirmation
class ResetEmailForm(FlaskForm):

    submit = SubmitField('Confirm Email Reset')


# Password reset request
class RequestPWResetForm(FlaskForm):

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    # To validate email exists in database
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()  # search for email in database
        if user is None:  # does user exist
            raise ValidationError('No account found with this email.')


# Password reset
class ResetPasswordForm(FlaskForm):

    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirmpassword = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
