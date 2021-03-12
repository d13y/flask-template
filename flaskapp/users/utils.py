import secrets
import os
from PIL import Image
from flask import url_for, current_app
from flask_login import current_user
from flask_mail import Message
from flaskapp import mail


# Save picture function
def save_picture(form_picture):

    random_hex = secrets.token_hex(8)  # generate random file name
    _, f_ext = os.path.splitext(form_picture.filename)  # identify current picture extension
    picture_fn = random_hex + f_ext  # combine random file name and extension
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)  # full path to directory

    output_size = (125, 125)  # resize image constraints (creates uniformity and saves space)
    img = Image.open(form_picture)  # access image
    img.thumbnail(output_size)  # resize image
    img.save(picture_path)  # save picture to directory

    return picture_fn


# Delete picture function
def delete_picture():

    old_picture = current_user.image_file  # identify current picture

    if old_picture != 'default.jpg':
        delete_picture_path = os.path.join(current_app.root_path, 'static/profile_pics', old_picture)  # identify path
        os.remove(delete_picture_path)  # delete picture from directory


# Send registration email
def sendemail_auth(newuser):

    token = newuser.get_auth_token_email()  # generate unique token
    msg = Message('Account Registration',  # subject
                  sender='noreply@flaskapp.com',  # sender (from)
                  recipients=[newuser.email])  # recipient (to)
    msg.body = f'''Verify account registration:
{url_for('users.auth_token', token=token, _external=True)}

If you did not make this request, then ignore this email and no actions will be taken.
'''
    mail.send(msg)  # send email


# Send registration email
def sendemail_emailreset(new_email):

    token = new_email.get_auth_token_email()  # generate unique token
    msg = Message('Email Reset Request',  # subject
                  sender='noreply@flaskapp.com',  # sender (from)
                  recipients=[new_email.temp_email])  # recipient (to)
    msg.body = f'''Confirm request to update email:
{url_for('users.reset_token_email', token=token, _external=True)}

If you did not make this request, then ignore this email and no changes will be taken.
'''
    mail.send(msg)  # send email


# Send password reset email
def sendemail_pwreset(user):

    token = user.get_reset_token_pw()  # generate unique token
    msg = Message('Password Reset Request',  # subject
                  sender='noreply@flaskapp.com',  # sender (from)
                  recipients=[user.email])  # recipient (to)
    msg.body = f'''Reset password:
{url_for('users.reset_token_pw', token=token, _external=True)}

If you did not make this request, then ignore this email and no changes will be made.
'''
    mail.send(msg)  # send email
