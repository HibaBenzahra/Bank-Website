from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
from flask_migrate import Migrate
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
from datetime import timedelta


app = Flask(__name__)

#configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/bank_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '9975cb7b31ab210770abf5dc'

# ------- email configuration ----------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # for gmail
app.config['MAIL_USERNAME'] = 'benzahra.hiba@gmail.com'
app.config['MAIL_PASSWORD'] = 'b u k a o b w w c e a h t u p s'  # my own app password
app.config['MAIL_PORT'] = 587  # Use 465 for SSL or 587 for TLS
app.config['MAIL_USE_TLS'] = True  # Enable TLS encryption
app.config['MAIL_USE_SSL'] = False  # Set to True if you're using SSL instead of TLS


#-------- session


app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # 30 minutes timeout
app.config['SESSION_PERMANENT'] = True  # Enable permanent sessions

#initialize database
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
admin = Admin(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'

mail = Mail(app)
s = URLSafeTimedSerializer(app.config["SECRET_KEY"])


#A MUST
from bank import routes