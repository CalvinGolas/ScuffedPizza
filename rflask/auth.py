import functools, re

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from rflask.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method =='POST':
        email = request.form['email']
        password = request.form['password']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        phoneNumber = request.form['phoneNumber']
        stateID = request.form['stateID']
        deliveryLocation = request.form['deliveryLocation']
        zipCode = request.form['zipCode']
        creditCard = request.form['creditCard']
        expirationDate = request.form['expirationDate']
        cvv = request.form['cvv']
        city = request.form['city']

        db = get_db()
        error = [None]

        if not firstName:
            error = 'First name is required.'
        elif not lastName:
            error = 'Last name is required.'
        elif not phoneNumber:
            error = 'Phone number is required.'
        elif not stateID:
            error = 'State ID is required.'
        elif not deliveryLocation:
            error = 'Delivery location is required.'
        elif not zipCode:
            error = 'Zip code is required.'
        elif not creditCard:
            error = 'Credit card is required.'
        elif not expirationDate:
            error = 'Expiration date is required.'
        elif not cvv:
            error = 'Cvv is required.'
        elif not city:
            error = 'City is required.'
        elif not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE email = ?', (email,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(email)

        if error is None:
            db.execute(
                'INSERT INTO user (email, password, firstName, lastName, phoneNumber, stateID, deliveryLocation, zipCode, creditCard, expirationDate, cvv, city) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (email, generate_password_hash(password), firstName, lastName, phoneNumber, stateID, deliveryLocation, zipCode, creditCard, expirationDate, cvv, city)
            )
            db.commit()
            return redirect(url_for('auth.login'))

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