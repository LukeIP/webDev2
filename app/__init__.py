# Univeristy of Leeds (2023)
# [Code] [Last Accessesd 26/10/2023]
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_babel import Babel
from flask_security import Security
from flask_security import SQLAlchemySessionUserDatastore
#from app.models import User, Role

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

migrate = Migrate(app, db)

babel = Babel(app)

# user_datastore = SQLAlchemySessionUserDatastore(db.session,
#                                                 User, Role)
# security = Security(app, user_datastore)

admin = Admin(app)


from app import views, models
