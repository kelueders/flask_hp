from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from hp_collection.forms import CharacterForm
from hp_collection.models import Character, db

prof = Blueprint('prof', __name__, template_folder='profile_templates')

@prof.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    characterform = CharacterForm()

    try:
        if request.method == 'POST' and characterform.validate_on_submit():

            name = characterform.name.data
            description = characterform.description.data
            house = characterform.house.data
            nationality = characterform.nationality.data
            occupation = characterform.occupation.data
            books_appeared_in = characterform.books_appeared_in.data
            user_token = current_user.token

            character = Character(name, description, house, nationality, occupation, 
                                  books_appeared_in, user_token)

            db.session.add(character)
            db.session.commit()

            return redirect(url_for('prof.profile'))
        
    except:
        raise Exception('Character not created. Please check your form and try again.')
    
    user_token = current_user.token
    characters = Character.query.filter_by(user_token = user_token)

    return render_template('profile.html', form = characterform, characters = characters)