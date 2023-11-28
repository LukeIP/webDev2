# Univeristy of Leeds (2023)
# [Code] [Last Accessesd 26/10/2023]
from config import SQLALCHEMY_DATABASE_URI
from app import db
import os.path

db.create_all()
