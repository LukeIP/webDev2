# Univeristy of Leeds (2023)
# [Code] [Last Accessesd 26/10/2023]
import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True

WTF_CSRF_ENABLED = True
# if in prod these would be set to a more secure method and use 
# environment variables
SECRET_KEY = 'a-very-secret-secret'
