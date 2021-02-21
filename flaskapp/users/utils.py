import secrets
import os
from PIL import Image
from flask import url_for, current_app
from flask_login import current_user
from flask_mail import Message
from flaskapp import mail


# Save picture function
def save_picture(form_picture):

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_fn


# Delete picture function
def delete_picture():

    old_picture = current_user.image_file
    delete_picture_path = os.path.join(current_app.root_path, 'static/profile_pics', old_picture)

    os.remove(delete_picture_path)


# Send reset email
def send_auth_email(newuser):

    token = newuser.get_emailauth_token()
    msg = Message('Account Verification',
                  sender='noreply@flaskapp.com',
                  recipients=[newuser.email])
    msg.body = f'''Verify account registration link:
{url_for('users.auth_token', token=token, _external=True)}

If you did not make this request, then ignore this email and no actions will be taken.
'''
    mail.send(msg)


# Send reset email
def send_pwreset_email(user):

    token = user.get_pwreset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@flaskapp.com',
                  recipients=[user.email])
    msg.body = f'''Reset password link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, then ignore this email and no changes will be made.
'''
    mail.send(msg)
