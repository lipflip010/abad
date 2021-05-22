# auth.py
from flask import Blueprint, redirect, url_for, render_template, request, flash
from flask_login import login_required, logout_user, login_user
from werkzeug.security import check_password_hash

from app.models import User

auth = Blueprint('auth', __name__)


@auth.context_processor
def get_current_user():
    from abad import hostname
    return {"hostname": hostname}


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))  # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.commands'))
