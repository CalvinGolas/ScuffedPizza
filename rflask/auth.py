import functools, re

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from rflask.db import get_db
from . import gali
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        phoneNumber = request.form['phoneNumber']
        stateID = request.form['stateID']
        deliveryLocation = request.form['deliveryLocation']
        zipCode = request.form['zipCode']
        cardID = request.form['cardID']
        gUsername = request.form['gUsername']
        gPassword = request.form['gPassword']
        accountNumber = request.form['accountNumber']
        city = request.form['city']

        db = get_db()
        error = []

        if not firstName:
            error.append('First name is required.')
        elif len(firstName) < 2:
            error.append('First name is too short, must be at least two characters')
        elif len(firstName) >= 15:
            error.append('First name is too long, must be less than 16 characters')
        elif re.match(re.compile("^[a-zA-Z]+[-]{0,1}[a-zA-Z]*$"), firstName) is None:
            error.append('First name must use alphabetical characters, a hyphen is permitted')
        if not firstName:
            error.append('Last name is required.')
        elif len(lastName) < 2:
            error.append('Last name is too short, must be at least two characters')
        elif len(lastName) >= 15:
            error.append('Last name is too long, must be less than 16 characters')
        elif re.match(re.compile("^[a-zA-Z]+[-]{0,1}[a-zA-Z]*$"), lastName) is None:
            error.append('Last name must use alphabetical characters, a hyphen is permitted')
        if not phoneNumber:
            error.append('Phone number is required.')
        elif re.match(re.compile("^[0-9]{10}$"), phoneNumber) is None:
            error.append('Phone number is invalid, please input a sequence of 10 integers')
        if not stateID:
            error.append('State ID is required.')
        elif re.match(re.compile("^[A-Z]{2}$"), stateID) is None:
            error.append('State ID should be two capital letters.')
        if not deliveryLocation:
            error.append('Delivery location is required.')
        if not zipCode:
            error.append('Zip code is required.')
        elif re.match(re.compile("^[0-9]{5}$"), zipCode) is None:
            error.append('Zip code is invalid, please submit a 5 digit integer code.')
        if not city:
            error.append('City is required.')
        if not email:
            error.append('Email is required.')
        if not password:
            error.append('Password is required.')
        if not gUsername:
            error.append('Galileo username is required.')
        if not gPassword:
            error.append('Galileo password is required.')
        if not cardID:
            error.append('Galileo card id is required.')
        if not accountNumber:
            error.append('Galileo account number is required.')
        if not error:
            if db.execute(
                    'SELECT id FROM user WHERE email = ?', (email,)
            ).fetchone() is not None:
                error = 'User {} is already registered.'.format(email)

            else:
                db.execute(
                    'INSERT INTO user (email, password, firstName, lastName, phoneNumber, stateID, deliveryLocation, '
                    'zipCode, city, gUsername, gPassword, cardID, accountNumber) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (email, generate_password_hash(password), firstName, lastName, phoneNumber, stateID, deliveryLocation,
                     zipCode, city, gUsername, gPassword, cardID, accountNumber)
                )

                db.commit()
                return redirect(url_for('auth.login'))
        if error is not []:
            flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone()

        if user is None:
            error = 'Incorrect email.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('getpied.getpie'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth_login'))
        return view(**kwargs)

    return wrapped_view
