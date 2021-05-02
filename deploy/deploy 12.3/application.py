import os
import uuid
import hashlib
import datetime as dt
from flask import Flask, session, render_template, url_for, redirect, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, CommentForm, PaymentForm, ProfileForm
from models import db, User, Payments, PaymentsTable, Comments
from functools import wraps

application = Flask(__name__)

# App Config
application.config['SECRET_KEY'] = os.environ.get('PORTAL_SECRET', str(uuid.uuid4()))
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portal.db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.app_context().push()
db.init_app(application)

def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
            if not session.get('username'):
                print("Invalid session! Returning to login")
                return redirect(url_for('login'))
            else:
                username = session.get('username')
                print(f"Valid session with {username}")     
                return f(username, *args, **kws)        
    return decorated_function

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm(csrf_enabled=False)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        raw_hash = hashlib.sha256(password.encode())
        str_hash = raw_hash.hexdigest()

        result = db.engine.execute(f"SELECT * FROM Users WHERE username='{username}' AND password='{str_hash}'")
        user = [row[0] for row in result]

        if not user:
            print(f"[!] Username {username} failed to login")
        else:
            print(f"[*] Username {username} logged in successfully")
            session['username'] = username
            return redirect(url_for('welcome'))
        
    return render_template('login.html', form=form)

@application.route('/welcome', methods = ['GET', 'POST'])
@authorize
def welcome(username):
    user = User.query.filter_by(username=username).first()
    first_name = user.first_name
    loan_balance = user.current_loan_balance

    today = dt.datetime.now()
    short_date = today.strftime("%B %Y")

    return render_template('welcome.html', name=first_name, loan_balance=loan_balance, date=short_date)

@application.route('/paynow', methods = ['GET'])
@authorize
def pay_now(username):
    form = PaymentForm(csrf_enabled=False)
    if form.validate_on_submit():
        billing_name = form.billing_address.data
        billing_address = form.billing_address.data
        billing_state = form.billing_state.data
        billing_zip = form.billing_zip.data
        cc_number = form.cc_number.data 
        exp_date = form.exp_date.data

    return render_template('pay_now.html', form=form)

@application.route('/payments', methods = ['GET'])
@authorize
def payments(username):
    user = User.query.filter_by(username=username).first()
    payments = Payments.query.filter_by(user_id=user.id).all()
    payments_table = PaymentsTable(payments)

    return render_template('payment_history.html', payments_table=payments_table)

@application.route('/support', methods = ['GET', 'POST'])
@authorize
def support(username):
    user = User.query.filter_by(username=username).first()
    stored_comments = Comments.query.filter_by(user_id=user.id).all()
    form = CommentForm(csrf_enabled=False)
    if form.validate_on_submit():
        print(form.submit.data)
        print(form.delete.data)

        if form.submit.data:
            date = dt.datetime.utcnow().strftime('%B %d, %Y')
            user_id = user.id
            message = form.message.data
            comment = Comments(user_id, date, message)
            comment.insert()
            return redirect(url_for('support'))
        elif form.delete.data:
            db.session.query(Comments).filter(Comments.user_id==user.id).delete()
            db.session.commit()
            return redirect(url_for('support'))
        else:
            pass

    return render_template('support.html', form=form, comments=stored_comments, username=username)

@application.route('/profile', methods = ['GET', 'POST'])
@authorize
def profile(username):
    user = User.query.filter_by(username=username).first()
    form = ProfileForm(csrf_enabled=False)

    if request.method == "GET":
        form.process(obj=user)
        form.hash_validation.data = hashlib.md5(str(user.current_loan_balance).encode('utf-8')).hexdigest()
        return render_template('profile.html', form=form)

    if request.method == "POST":
        if form.validate_on_submit():
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.address = form.address.data
            user.occupation = form.occupation.data
            user.current_loan_balance = form.current_loan_balance.data

            user_provided_hash = form.hash_validation.data.lower()
            expected_hash = hashlib.md5(str(form.current_loan_balance.data).encode('utf-8')).hexdigest()

            if user_provided_hash == expected_hash:
                print("Validation succeeded!")
                user.update()
            else:
                print(f"Hash failed - user provided {user_provided_hash} when {expected_hash} was expected")
                abort(500)
    return redirect(url_for("profile"))


@application.route('/releases', methods = ['GET'])
def releases():
    return "v1.3.0 App Bug Fix: Removed redirect on failed login, wasn't needed and was confusing our users<br/>\
    v1.2.0 App Bug Fix: Don't forget to fix that security issue with the DB. We really need to stop using SQLite databases..."

@application.route('/logout', methods = ['GET'])
def logout():
    session.clear()
    return redirect(url_for('index'))

@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@application.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    (application.run(host='0.0.0.0', debug=True))