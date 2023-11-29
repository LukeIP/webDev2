# Univeristy of Leeds (2023)
# [Code] [Last Accessesd 26/10/2023]
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

migrate = Migrate(app, db)

admin = Admin(app,template_mode='bootstrap4')

from app import views, models
