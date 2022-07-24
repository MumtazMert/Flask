from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)
from .models import User

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
            #Email validation in database
        user= User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True) #Remembering user 
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect! Please try again', category='error')
        else:
            flash('Email does not exist', category='error')
    return render_template('login.html', user=current_user)

@auth.route("/logout")
@login_required #User cant logout if didn't login
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/sign-up", methods=['GET', 'POST'])

def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
            #Validation check
        
        user= User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists' , category='success')
        if len(email) < 4:
            flash('Email must be at least 4 characters', category='error')
        elif len('first_name') < 2:
            flash('First name must be at least 2 characters', category='error')
        elif password1 != password2:
            flash ('Passwords must match', category='error')
        elif len('password1') < 5:
            flash('Password must be at least 5 characters', category='error')
        else:
            #Creating new user 
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('sign-up.html', user=current_user)