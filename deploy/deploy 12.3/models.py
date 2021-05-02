from flask_sqlalchemy import SQLAlchemy
from flask_table import Table, Col

db = SQLAlchemy()

class User(db.Model):
    __tablename__ ='Users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(80))
    password = db.Column(db.Text)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    address = db.Column(db.String(80))
    occupation = db.Column(db.String(30))
    loan_product = db.Column(db.String(30))
    starting_loan_balance = db.Column(db.Integer)
    current_loan_balance = db.Column(db.Integer)

    def __init__(self, id, username, password, first_name, last_name, address, occupation, loan_product, starting_loan_balance, current_loan_balance):
        self.user_id = id
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.occupation = occupation
        self.loan_product = loan_product
        self.starting_loan_balance = starting_loan_balance
        self.current_loan_balance = current_loan_balance

    def update(self):
        db.session.add(self)
        db.session.commit()
        print("Updated user")


class Payments(db.Model):
        __tablename__ ='Payments'
        payment_id = db.Column(db.Integer,primary_key = True)
        user_id = db.Column(db.Integer,db.ForeignKey('User.id'))
        date = db.Column(db.String(80))
        amount = db.Column(db.Integer)

class PaymentsTable(Table):
    classes = ['table']
    payment_id = Col('Transaction ID')
    date = Col('Payment Date')
    amount = Col('Amount ($)')

class Comments(db.Model):
    __tablename__='Comments'
    comment_id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('Users.id'))
    date = db.Column(db.String(80))
    message = db.Column(db.String(1024))

    def __init__(self, user_id, date, message):
        self.user_id = user_id
        self.date = date
        self.message = message

    def insert(self):
        db.session.add(self)
        db.session.commit()
