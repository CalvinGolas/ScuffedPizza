from flask import (
    Blueprint, flash, g, session, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from . import gali
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
@login_required
def getpie():
    currentId = session.get('user_id')
    db = get_db()
    if request.method == 'POST':
        name = db.execute('SELECT * FROM user WHERE id = ?', (currentId,)).fetchone()


        # galileo sweetness
        newPerson = gali.Galigali(name[10], name[11], name[12], name[13])
        newPerson.setAccessToken()
        newPerson.transactionId = newPerson.randomString(30)
        if db.execute('SELECT COUNT(*) FROM SpendingAccount').fetchone()[0] < 1:
            db.execute('INSERT INTO SpendingAccount (rpn) VALUES (?)', (newPerson.setSpendingAccount(),))
            print("successful insertion")
        else:
            newPerson.spending_account = db.execute('SELECT rpn FROM SpendingAccount WHERE id = 1').fetchone()[0]

        newPerson.transfer(newPerson.transactionId)


        message = client.messages \
            .create(
            body=("Medium cheese pizza ordered for " + name[3] + "! Please deliver to " + name[7] + ", " + name[9] + " " + name[6] + ", " + name[8] + "."),
            from_='+12562516142',
            to='+18054539083'
        )
        print("Message: ", message.sid)

        return redirect(url_for('getpied.gotpie'))
    return render_template('getpie/lessago.html')

@bp.route('/gotpie', methods=['GET', 'POST'])
@login_required
def gotpie():
    db = get_db()
    return render_template('getpie/weagot.html')