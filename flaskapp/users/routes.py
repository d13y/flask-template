from datetime import datetime
from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, current_user, login_required
from flaskapp import db, bcrypt
from flaskapp.models import User
from flaskapp.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                  RequestPWResetForm, ResetPasswordForm,
                                  ResetEmailForm)
from flaskapp.users.utils import (save_picture, delete_picture,
                                  sendemail_auth, sendemail_pwreset, sendemail_emailreset)


users = Blueprint('users', __name__)  # setup blueprint for 'user' directory


# Registration page
@users.route("/register", methods=['GET', 'POST'])
def register():

    # If user is already logged in, return to home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    # Set form variable to registration form
    form = RegistrationForm()

    # Only run following code if form response passes checks (in users/forms.py)
    if form.validate_on_submit():

        # Remove old user info if exists (and unvalidated)
        olduser = User.query.filter(User.username.ilike(f'%{form.username.data}%')).first()  # check if username exists
        if olduser and olduser.confirm_account is False:  # remove username
            db.session.delete(olduser)  # delete row entry
            db.session.commit()  # save changes
        oldemail = User.query.filter(User.email.ilike(f'%{form.email.data}%')).first()  # check for email in db
        if oldemail and oldemail.confirm_account is False:  # remove email
            db.session.delete(oldemail)  # delete row entry
            db.session.commit()  # save changes

        # Add user to db
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # encrypt password
        newuser = User(username=form.username.data, email=form.email.data, password=hashed_pw, date_register=datetime.now()) # noqa
        db.session.add(newuser)  # add row entry
        db.session.commit()  # save changes
        sendemail_auth(newuser)  # send authentication email

        # Inform user that email authentication is required
        flash(f'Email verification request sent to {form.email.data}!', 'success')
        return redirect(url_for('users.login'))

    return render_template('register.html', title='Register', form=form)  # key variables for .html


# Verify email function
@users.route("/register/<token>", methods=['GET', 'POST'])
def auth_token(token):

    # If user is already logged in, return to home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    # Verify if URL includes valid token
    user = User.verify_auth_token_email(token)

    # Handle if URL is (not) valid
    if user is None:  # if not valid
        flash(f'Token invalid or expired.', 'warning')
        return redirect(url_for('users.register'))
    else:  # if valid
        user.confirm_account = True  # record that email/account is verified
        user.date_verify = datetime.now()  # record verified date/time
        db.session.commit()  # save changes
        # Inform user that email has been verified has been reset
        flash(f'Email verified!', 'success')
        return redirect(url_for('users.login'))


# Login page
@users.route("/login", methods=['GET', 'POST'])
def login():

    # If user is already logged in, return to home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    # Set form variable to login form
    form = LoginForm()

    # Only run following code if form response passes checks (in users/forms.py)
    if form.validate_on_submit():

        user = User.query.filter(User.email.ilike(f'%{form.email.data}%')).first()  # check for email in db

        # Check that account info is correct, and email is verified
        if user and bcrypt.check_password_hash(user.password, form.password.data):  # check password
            if user.confirm_account:  # check email verification
                login_user(user, remember=form.remember.data)  # login user
                prev_page = request.args.get('next')
                return redirect(prev_page) if prev_page else redirect(url_for('main.home'))  # return user to home page
            else:  # if email not yet verified
                flash(f'Account not verified. Please check emails for instructions.', 'warning')
        else:  # if login details are incorrect
            flash(f'Login unsuccessful. Please check details.', 'danger')

    return render_template('login.html', title='Login', form=form)  # key variables for .html


# Logout page
@users.route("/logout")
def logout():
    logout_user()  # logout function
    return redirect(url_for('main.home'))


# Account page
@users.route("/account", methods=['GET', 'POST'])
@login_required  # ensures account page is only returned if user is logged in
def account():

    # Set form variable to account page form
    form = UpdateAccountForm()

    # Only run following code if form response passes checks (in users/forms.py)
    if form.validate_on_submit():

        # Only run following code if new picture uploaded
        if form.picture.data:
            delete_picture()  # delete old picture
            picture_file = save_picture(form.picture.data)  # upload new picture
            current_user.image_file = picture_file  # update user display
            flash('Profile picture updated!', 'success')

        # Remove old user info if exists (and unvalidated)
        olduser = User.query.filter(User.username.ilike(f'%{form.username.data}%')).first()  # check for username in db
        if olduser and olduser.confirm_account is False:  # remove username
            db.session.delete(olduser)  # delete row entry
            db.session.commit()  # save changes
        oldemail = User.query.filter(User.email.ilike(f'%{form.email.data}%')).first()  # check for email in db
        if oldemail and oldemail.confirm_account is False:  # remove email
            db.session.delete(oldemail)  # delete row entry
            db.session.commit()  # save changes

        # Update username
        if form.username.data != current_user.username:
            current_user.username = form.username.data
            db.session.commit()
            flash('Username updated!', 'success')

        # Send email to verify change
        if form.email.data != current_user.email:
            current_user.temp_email = form.email.data  # update temp email
            db.session.commit()
            newemail = User.query.filter_by(temp_email=form.email.data).first()
            sendemail_emailreset(newemail)  # send email to new change
            flash('Email reset request sent!', 'success')

        # Save changes
        db.session.commit()  # save changes

        return redirect(url_for('users.account'))

    # Return original account page, if no form/changes submitted (i.e. before update)
    elif request.method == 'GET':
        form.username.data = current_user.username  # display current username
        form.email.data = current_user.email  # display current email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)  # display user profile pic

    return render_template('account.html', title='Account', image_file=image_file, form=form)  # key variables for .html


# Reset password function
@users.route("/resetemail/<token>", methods=['GET', 'POST'])
@login_required  # ensure user is logged in before changing associated email
def reset_token_email(token):

    # Verify if URL includes valid token
    user = User.verify_auth_token_email(token)

    # Handle if URL is (not) valid
    if user is None:
        flash('Token invalid or expired.', 'warning')  # display message
        return redirect(url_for('users.login'))

    form = ResetEmailForm()

    if form.validate_on_submit():
        # Replace email with updated email
        current_user.email = current_user.temp_email  # set new email
        current_user.temp_email = None  # reset temp_email field
        db.session.commit()  # save changes

        # Inform user that email has been changed
        flash(f'Email changed!', 'success')
        return redirect(url_for('users.login'))

    return render_template('reset_token_email.html', title='Reset Email', form=form)  # key variables for .html


# Reset password request
@users.route("/resetpassword", methods=['GET', 'POST'])
def reset_request_pw():

    # If user is already logged in, return to home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    # Set form variable to password reset request page form
    form = RequestPWResetForm()

    # Only run following code if form response passes checks (in users/forms.py)
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()  # search for email in database
        sendemail_pwreset(user)  # send password reset email, if email found
        flash('Password reset email sent! Please check junk email folder.', 'success')
        return redirect(url_for('users.login'))

    return render_template('reset_request_pw.html', title='Reset Password', form=form)  # key variables for .html


# Reset password function
@users.route("/resetpassword/<token>", methods=['GET', 'POST'])
def reset_token_pw(token):

    # If user is already logged in, return to home page
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    # Verify if URL includes valid token
    user = User.verify_reset_token_pw(token)

    # Handle if URL is not valid
    if user is None:
        flash('Token invalid or expired.', 'warning')  # display message
        return redirect(url_for('users.reset_request_pw'))

    # Set form variable to password reset page form
    form = ResetPasswordForm()

    # Only run following code if form response passes checks (in users/forms.py)
    if form.validate_on_submit():

        # Add user to db
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # encrypt password
        user.password = hashed_pw  # set new password
        db.session.commit()  # save changes

        # Inform user that password has been reset
        flash(f'Password reset for {form.username.data}!', 'success')
        return redirect(url_for('users.login'))

    return render_template('reset_token_pw.html', title='Reset Password', form=form)  # key variables for .html
