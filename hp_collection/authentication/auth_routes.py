from flask import Blueprint, render_template, request, redirect, url_for, flash
from hp_collection.forms import UserLoginForm
from hp_collection.models import User, db
from werkzeug.security import check_password_hash

from flask_login import login_user, logout_user, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    userform = UserLoginForm()

    try:
        if request.method == 'POST' and userform.validate_on_submit():
            email = userform.email.data
            username = userform.username.data
            password = userform.password.data
            print(email, password)

            user = User(email, username, password)   
            
            db.session.add(user)
            db.session.commit()

            flash(f'You have successfully created a user account for {email}', 'user-created')

            return redirect(url_for('auth.signin'))
        
    except:
        raise Exception('Invalid Form Data. Please check your form.')
    
    return render_template('signup.html', form = userform)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    userform = UserLoginForm()

    try:
        if request.method == "POST" and userform.validate_on_submit():
            email = userform.email.data
            username = userform.username.data
            password = userform.password.data
            print(email, username, password)


            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('You were successfully signed in via: Email/Password', 'auth-success')
                return redirect(url_for('prof.profile'))
            else:
                flash('Your Email/Password is incorrect', 'auth-failed')
                return redirect(url_for('auth.signin'))
            
    except:
        raise Exception('Invalid Form Data: Please Check Your Form')

    return render_template('signin.html', form = userform)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('general.home'))