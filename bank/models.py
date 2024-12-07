from bank import db, admin
from datetime import datetime
from bank import bcrypt
from bank import login_manager
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import Select2Widget
from wtforms import SelectField
from wtforms import validators
from wtforms_sqlalchemy.fields import QuerySelectField


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    phone_number = db.Column(db.String(length=15), nullable=False)  
    address = db.Column(db.String(length=100), nullable=False)
    password = db.Column(db.String(length=100), nullable=False)  # For hashed passwords
    date_opened = db.Column(db.DateTime, default=datetime.utcnow)  # Date user account was created
    
    #relationship with 'Account' model
    accounts = db.relationship('Account', back_populates="user")

    def __str__(self):
        return self.username


    @property
    def hashing(self):
        return self.password
    
    @hashing.setter
    def hashing(self, plaintext_password):
        self.password = bcrypt.generate_password_hash(plaintext_password).decode('utf-8')

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)
    

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(length=30), nullable=False)
    balance = db.Column(db.Integer, nullable=False)
    date_opened = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(length=30), nullable=False)  

    # Foreign Key to link Account to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    user= db.relationship("User", back_populates="accounts") 

    def __str__(self):
        return self.type

    #relationship with Transaction model acc_id
    transactions = db.relationship('Transaction', backref='acc', lazy=True, foreign_keys='Transaction.acc_id')
    #relationship with Transaction model destinated_acc
    incoming_transactions = db.relationship('Transaction', 
                                            backref='destinated_acc', 
                                            lazy=True, 
                                            foreign_keys='Transaction.destinated_acc_id')

class UserView(ModelView):
    column_list = ['username', 'email', 'phone_number', 'address', 'date_opened', 'accounts']
    column_filters = ['username', 'email']
    column_searchable_list = ['username', 'email']
    form_excluded_columns = ['password']  # Exclude hashed password from being directly editable     


class AccountView(ModelView):
    # Specify columns to display in the admin panel
    column_list = ["type", "balance", "date_opened", "status", "user"]

    # Configure form columns to edit the account model
    form_columns = ["type", "balance", "date_opened", "status", "user"]

    # Custom form field definitions
    form_extra_fields = {
        'user': QuerySelectField(
            'User',
            query_factory=lambda: User.query.all(),
            get_label="username",  # Display the username in the dropdown
            allow_blank=False,     # Ensure the user field is required
            widget=Select2Widget(),
        ),
        'type': SelectField(
            'Account Type',
            choices=[("Savings", "Savings"), ("Checking", "Checking"), ("Business", "Business")],
            widget=Select2Widget(),
        ),
        'status': SelectField(
            'Status',
            choices=[("Active", "Active"), ("Inactive", "Inactive"), ("Closed", "Closed")],
            widget=Select2Widget(),
        ),
    }




class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(length=30), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    #Foreign Key to link Transaction to Account user
    acc_id = db.Column(db.Integer, db.ForeignKey('account.id'))

    #Foreign Key to link Transaction to destinated Account 
    destinated_acc_id = db.Column(db.Integer, db.ForeignKey('account.id'))


admin.add_view(UserView(User, db.session))
admin.add_view(AccountView(Account, db.session)) 

