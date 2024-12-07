from bank.models import User, Account, Transaction
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from flask_login import current_user


class RegisterForm(FlaskForm):
    # validate that username is unique
    def validate_name(self, name_tocheck):
        user = User.query.filter_by(username=name_tocheck.data).first()
        if user:
            raise ValidationError('Name already exists, Please try another one!')

    def validate_email(self, email_tocheck):
        user = User.query.filter_by(email=email_tocheck.data).first()
        if user:
            raise ValidationError('Email already exists, Please try another one!')
    
    def validate_phone(self, phone_tocheck):
        user = User.query.filter_by(phone_number=phone_tocheck.data).first()
        if user:
            raise ValidationError('Phone Number already exists, Please try another one!')
           
    
    name = StringField(label= 'Name', validators=[DataRequired(), Length(min=8, max=30)])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    phone = StringField(label='Phone', validators=[DataRequired(), Length(min=10, max=15)])
    address = StringField(label='Address', validators=[DataRequired(), Length(min=5, max=100)])
    password1 = PasswordField(label='Password', validators=[DataRequired(), Length(min=8, max=100)])
    password2 = PasswordField(label='Confirm Password', validators=[DataRequired(), EqualTo('password1')])
    submit = SubmitField(label='Register')


class LoginForm(FlaskForm):
    
    name = StringField(label= 'Name', validators=[DataRequired(), Length(min=8, max=30)])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8, max=100)])
    submit = SubmitField(label='Login')

class TransactionForm(FlaskForm):
    type = SelectField(
    'Transaction Type',
    choices=[('transfer', 'Transfer')],validators=[DataRequired()])
    from_acc = StringField(validators=[DataRequired(), Length(min=8, max=30)])
    recipient = StringField(validators=[DataRequired()])
    amount = StringField(validators=[DataRequired(), Length(min=2, max=6)])
    submit = SubmitField(label='Submit Transaction')

    
    def validate_from_acc(self, from_acc_tocheck):
        from_account = Account.query.filter_by(type=from_acc_tocheck.data, user_id = current_user.id).first()
        if not from_account:
            raise ValidationError("You don't such account, Please try another one!")
    
    def validate_recipient(self, recipient_tocheck):
        to_account = Account.query.filter_by(id=recipient_tocheck.data).first()
        if not to_account:
            raise ValidationError("This recipient account doesn't exist, Please try another one!")
        
    def validate_amout(self, amount_tocheck):
        if amount_tocheck <= 0:
            raise ValidationError("Amount must be positive!")




#class AccountForm(FlaskForm):


