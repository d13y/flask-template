from flask import Blueprint, render_template

main = Blueprint('main', __name__)  # setup blueprint for 'main' directory


# Home page
@main.route("/")
def home():
    return render_template('home.html', title='Home')
