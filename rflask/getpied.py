from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from rflask.auth import login_required
from rflask.db import get_db
from twilio.rest import Client
account_sid = 'ACb4fd4758c8add7efc0481cd961e48084'
auth_token = '37bae9b4bf498690ec0e3ffcce1eb3f6'
client = Client(account_sid, auth_token)

bp = Blueprint('getpied', __name__)

@bp.route('/')
def index():
    db = get_db()
    return render_template('getpie/index.html')

@bp.route('/getpie', methods=['GET', 'POST'])
def getpie():
    if request.method == 'POST':
        message = client.messages \
            .create(
            body="Anything is possible!",
            from_='+12562516142',
            to='+18054539083'
        )
        print("Message: ", message.sid)

        return redirect(url_for('getpied.gotpie'))
    return render_template('getpie/lessago.html')

@bp.route('/gotpie', methods=['GET', 'POST'])
def gotpie():
    db = get_db()
    return render_template('getpie/weagot.html')