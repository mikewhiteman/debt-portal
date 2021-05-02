from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, PasswordField, IntegerField, HiddenField
from wtforms.validators import InputRequired

class LoginForm(FlaskForm):
    username = StringField('Username: ', [InputRequired()])
    password = PasswordField('Password: ', [InputRequired()])
    submit = SubmitField('Login')

class CommentForm(FlaskForm):
    message = StringField('Message: ')
    submit = SubmitField('Submit')
    delete = SubmitField('Clear History')


class PaymentForm(FlaskForm):
    billing_name = StringField('Billing Name: ')
    billing_address = StringField('Address: ')
    billing_state = StringField('State: ')
    billing_zip = StringField('Zip: ')
    cc_number = StringField('Credit Card #: ')
    exp_date = StringField('Expiration Date: ')
    submit = SubmitField('Pay Now')

class ProfileForm(FlaskForm):
    username = StringField('Username: ')
    first_name = StringField('First Name: ')
    last_name = StringField('Last Name: ')
    address = StringField('Address: ')
    occupation = StringField('Occupation: ')
    loan_product = StringField('Loan Product: ')
    starting_loan_balance = IntegerField('Starting Loan Balance: ')
    current_loan_balance = IntegerField('Current Loan Balance: ')
    hash_validation = HiddenField('Hash: ')
    submit = SubmitField('Save Changes')