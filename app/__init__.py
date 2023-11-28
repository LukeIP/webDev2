# Univeristy of Leeds (2023)
# https://alt-6100e9398f586.blackboard.com/bbcswebdav/pid-11535312-dt-content-rid-38152052_2/courses/202324_32870_COMP2011/site/index.html
# [Code] [Last Accessesd 26/10/2023]
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from app import views, models
