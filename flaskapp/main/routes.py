from flask import Blueprint, render_template, request

main = Blueprint('main', __name__)


# Home page
@main.route("/")
def home():
    return render_template('home.html', title='Home')
