from bank import app, db, s, mail
from bank.forms import RegisterForm, LoginForm, TransactionForm
from flask import render_template, redirect, url_for, flash
from bank.models import User, Account, Transaction
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime 
from flask_mail import Message
from itsdangerous import SignatureExpired, BadSignature
from flask import session

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
            session['user_id'] = attempted_user.id
            session.permanent = True  # Use the lifetime set in config
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
        return redirect (url_for('confirm_email'))
    
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Error: {err_msg}', category='danger')

    return render_template("register.html", form=form)


@app.route('/transactions', methods=['GET', 'POST'])
@login_required
def transactions_page():
    form = TransactionForm()

    if form.validate_on_submit():
        from_account = Account.query.filter_by(type=form.from_acc.data, user_id=current_user.id).first()
        to_account = Account.query.filter_by(id=form.recipient.data).first()
        amount = int(form.amount.data)

        # Check if the from_account has sufficient balance
        if from_account.balance >= amount:
            # Perform the transaction
            from_account.balance -= amount
            to_account.balance += amount

            # Record the transaction
            transaction = Transaction(
                type=form.type.data,
                amount=amount,
                acc_id=from_account.id,
                destinated_acc_id=to_account.id,
                date=datetime.utcnow()
            )

            db.session.add(transaction)
            db.session.commit()

            flash(f"Transaction of {amount} MAD completed successfully.", category='success')
        else:
            flash("Insufficient balance for this transaction", category='danger')

    # Fetch transaction history
    transactions = Transaction.query.filter_by(acc_id=current_user.id).order_by(Transaction.date.desc()).all()
    return render_template("transactions.html", form=form, transactions=transactions)


#@app.route("/account")
#def account_page():

 #   return render_template("account.html")

@app.route('/logout')
def logout_page():
    logout_user()
    session.clear()  # Clear session data
    flash(f'You are now logged out!', category='info')
    return redirect(url_for("home_page"))

#Email verification 
@app.route('/confirm_email')
def confirm_email():

	email = current_user.email
	token = s.dumps(email, salt='email-confirm')

	msg = Message('Confirm Email', sender='benzahra.hiba@gmail.com', recipients=[email])
	link = url_for('checkout_success', token=token,  _external=True)
	msg.body = 'Click on this link for verification {}'.format(link)
	mail.send(msg)

	return render_template('email_confirm.html', email='email', token=token)

# Route for successful checkout page
@app.route('/checkout_success/<token>')
def checkout_success(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=600)
        flash(f'Your account have been successfully created!!', category='success')       
        return render_template('success.html')
    except SignatureExpired:
        return redirect(url_for('checkout_failure'))
	
    except BadSignature:
        return redirect(url_for('checkout_failure'))


# Route for failed checkout page
@app.route('/checkout_failure')
def checkout_failure():
    return render_template('failure.html')
