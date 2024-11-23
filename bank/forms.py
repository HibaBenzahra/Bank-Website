from bank.models import User, Account, Transaction
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError


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
    type = StringField(validators=[DataRequired(), Length(min=6, max=30)])
    from_acc = StringField(validators=[DataRequired(), Length(min=8, max=30)])
    recipient = StringField(validators=[DataRequired(), Length(min=8, max=30)])
    amount = StringField(validators=[DataRequired(), Length(min=2, max=6)])
    notes = TextAreaField( validators=[DataRequired(), Length(min=5, max=150)])
    submit = SubmitField(label='Submit Transaction')

#class AccountForm(FlaskForm):


