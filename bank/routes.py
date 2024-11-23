from bank import app, db
from bank.forms import RegisterForm, LoginForm, TransactionForm
from flask import render_template, redirect, url_for, flash
from bank.models import User, Account, Transaction
from flask_login import login_user, logout_user, login_required, current_user
import datetime 



@app.route('/')
@app.route('/home')
def home_page():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.name.data).first()
        if attempted_user and attempted_user.check_password(form.password.data):
            login_user(attempted_user)
            flash(f"You are now logged in {form.name.data}", category='success')
            return redirect(url_for('transactions_page'))
        else:
            flash("This user doesn't exist, Try another Username of Password!")


    return render_template("login.html", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_created = User(username= form.name.data, email=form.email.data, 
                            phone_number=form.phone.data, address=form.address.data,
                            hashing=form.password1.data)
        db.session.add(user_created)
        db.session.commit()
        login_user(user_created)
        flash(f'Your account have been successfully created, You are now Logged in {user_created.username}!!', category='success')
        return redirect (url_for('transactions_page'))
    
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Error: {err_msg}', category='danger')

    return render_template("register.html", form=form)


@app.route('/transactions')
@login_required
def transactions_page():
    form = TransactionForm()
    if form.validate_on_submit():
        from_account = Account.query.filter_by(account_number=form.from_acc.data, user_id=current_user.id).first()

        if not from_account:
            flash("Source account not found or you do not have access to this account", category='danger')
            return redirect(url_for('transactions_page'))


        to_account = Account.query.filter_by(account_number=form.recipient.data).first()

        if not to_account:
            flash("Recipient account not found", category='danger')
            return redirect(url_for('transactions_page'))


        transaction_type = form.type.data


        try:
            amount = int(form.amount.data)
        except ValueError:
            flash("Invalid amount entered", category='danger')
            return redirect(url_for('transactions_page'))

        if amount <= 0:
            flash("Amount must be positive", category='danger')
            return redirect(url_for('transactions_page'))


        if from_account.balance >= amount:

            from_account.balance -= amount

            to_account.balance += amount


            transaction = Transaction(
                type=transaction_type,
                amount=amount,
                acc_id=from_account.id,
                destinated_acc_id=to_account.id,
                date=datetime.utcnow()
            )


            db.session.add(transaction)
            db.session.commit()


            flash(f"Transaction of {amount} from {from_account.account_number} to {to_account.account_number} was successful", category='success')
        else:
            flash("Insufficient balance for this transaction", category='danger')

        return redirect(url_for('transactions_page'))
    return render_template("transactions.html", form=form)

#@app.route("/account")
#def account_page():

 #   return render_template("account.html")

@app.route('/logout')
def logout_page():
    logout_user()
    flash(f'You are now logged out!', category='info')
    return redirect(url_for("home_page"))