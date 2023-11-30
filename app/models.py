from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# linking tables
groups = db.Table('groups',
                  db.Column('user_id', db.String(500),
                            db.ForeignKey('user.id'), primary_key=True),
                  db.Column('group_id', db.Integer,
                            db.ForeignKey('group.id'), primary_key=True))
likes = db.Table('likes',
                 db.Column('user_id', db.String(500),
                           db.ForeignKey('user.id'), primary_key=True),
                 db.Column('post_id', db.Integer,
                           db.ForeignKey('post.id'), primary_key=True))


# DB Models
# User also inherits from flask_login usermixin so it has correct format
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(500), unique=True, nullable=False)
    name = db.Column(db.String(500), nullable=False)
    # __ used to mark it as a property that should not be edited directly
    __password_hash = db.Column(db.String(500))
    # one to many relationship
    posts = db.relationship('Post', backref='user')
    owned_groups = db.relationship('Group', backref='owner')

    # helper functions which should be used to set password
    def set_password(self, password):
        self.__password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.__password_hash, password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=True)
    likes = db.relationship('User', secondary=likes, backref='liked_posts')


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    posts = db.relationship('Post', backref='group')
    users = db.relationship('User', secondary=groups, backref='groups')
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
