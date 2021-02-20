from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, current_user, login_required
from flaskapp import db, bcrypt
from flaskapp.models import User
from flaskapp.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                  RequestResetForm, ResetPasswordForm)
from flaskapp.users.utils import (save_picture, delete_picture,
                                  send_auth_email, send_pwreset_email)


users = Blueprint('users', __name__)


# Registration page
@users.route("/register", methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        # Add user to db
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        newuser = User(username=form.username.data, email=form.email.data, password=hashed_pw) # noqa
        db.session.add(newuser)
        db.session.commit()
        send_auth_email(newuser)
        # Inform user that email authentication is required
        flash(f'Email verification request sent to {form.email.data}!', 'success')
        return redirect(url_for('users.login'))

    return render_template('register.html', title='Register', form=form)


# Verify email function
@users.route("/register/<token>", methods=['GET', 'POST'])
def auth_token(token):

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_emailauth_token(token)

    if user is None:
        flash(f'Token invalid or expired.', 'warning')
        return redirect(url_for('users.register'))
    else:
        user.email_confirm = True
        db.session.commit()
        # Inform user that email has been verified has been reset
        flash(f'Email verified for {User.email.data}!', 'success')
        return redirect(url_for('users.login'))


# Login page
@users.route("/login", methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.email.ilike(form.email.data)).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if user.email_confirm:
                login_user(user, remember=form.remember.data)
                prev_page = request.args.get('next')
                return redirect(prev_page) if prev_page else redirect(url_for('main.home'))
            else:
                flash(f'Account not verified. Please check emails for instructions.', 'danger')
        else:
            flash(f'Login unsuccessful. Please check details.', 'danger')

    return render_template('login.html', title='Login', form=form)


# Logout page
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


# Account page
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            delete_picture()
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account details updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)

    return render_template('account.html', title='Account', image_file=image_file, form=form)


# Reset password request
@users.route("/resetpassword", methods=['GET', 'POST'])
def reset_request():

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_pwreset_email(user)
        flash('Password reset email sent! Please check junk email folder.', 'success')
        return redirect(url_for('users.login'))

    return render_template('reset_request.html', title='Reset Password', form=form)


# Reset password function
@users.route("/resetpassword/<token>", methods=['GET', 'POST'])
def reset_token(token):

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_pwreset_token(token)

    if user is None:
        flash('Token invalid or expired.', 'warning')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        # Add user to db
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        # Inform user that password has been reset
        flash(f'Password reset for {form.username.data}!', 'success')
        return redirect(url_for('users.login'))

    return render_template('reset_token.html', title='Reset Password', form=form)
