from flask import render_template, request, flash, redirect, url_for, session
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, RegistrationForm

# Declaration: The programme writing of auth/routes.py studies the instruction in Book
# "FLASK Web Development: Developing Web Applications with Python, Second Edition"


# login method
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            if user.verify_password(form.password.data):
                flash('Sign in Success')
                session['USERNAME'] = user.username
                # utilize relative URL, in case of malevolent users damage.
                route_next = request.args.get('next')
                if route_next is None or not route_next.startswith('/'):
                    return redirect(url_for('main.main_page'))
                else:
                    return redirect(route_next)
            else:
                flash('Your username or password is not verified')
        else:
            flash('This user does not exist')
    return render_template('auth/login.html', form=form)


# register method
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.password.data != form.password2.data:
            flash('Passwords should match each other')
            return redirect(url_for('auth.register'))
        else:
            user_db = User.query.filter_by(username=form.username.data).first()
            if user_db:
                flash('This username has been register before, try a new one')
                return redirect(url_for('auth.register'))
            else:
                user = User(username=form.username.data, password=form.password.data)
                db.session.add(user)
                # commit first, so that user id can generated with token later
                db.session.commit()
                # redirect to login page
                return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


# This method helps user to log out
@auth.route('/logout')
def logout():
    session.pop('USERNAME', None)
    # flash a reminding message
    flash('You have been signed out.')
    # redirect to main page
    return redirect(url_for('main.main_page'))
