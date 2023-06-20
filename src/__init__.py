from decouple import config
from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

app = Flask(__name__)
app.config.from_object(config("APP_SETTINGS"))

login_manager = LoginManager() 
login_manager.init_app(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Registering blueprints
from src.accounts.views import accounts_bp
from src.core.views import core_bp

app.register_blueprint(accounts_bp)
app.register_blueprint(core_bp)

#the user_loader callback is used to reload the user object from the user ID stored in the session
from src.accounts.model import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

#customize the default login process 
login_manager.login_view = "accounts.login"
#customize the message category
login_manager.login_message_category = "danger"