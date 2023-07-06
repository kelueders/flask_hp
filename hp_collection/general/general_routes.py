from flask import Blueprint, render_template

general = Blueprint('general', __name__, template_folder='gen_templates')

@general.route('/')
def home():
    print("Welcome to a Harry Potter fan's dream come true!")
    return render_template('index.html')


