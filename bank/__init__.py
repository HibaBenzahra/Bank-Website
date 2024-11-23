from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
from flask_migrate import Migrate

app = Flask(__name__)


#configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/bank_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '9975cb7b31ab210770abf5dc'

#initialize database
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
admin = Admin(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'

#A MUST
from bank import routes