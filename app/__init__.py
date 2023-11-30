# Univeristy of Leeds (2023)
# [Code] [Last Accessesd 26/10/2023]
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_babel import Babel
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

migrate = Migrate(app, db)

babel = Babel(app)

login_manager = LoginManager()
login_manager.init_app(app)

admin = Admin(app)

from app import views, models
