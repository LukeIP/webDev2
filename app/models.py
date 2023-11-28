from app import db

# linking tables
groups = db.Table('groups',
                  db.Column('user_id', db.Integer,
                            db.ForeignKey('user.id'), primary_key=True),
                  db.Column('group_id', db.Integer,
                            db.ForeignKey('group.id'), primary_key=True))
likes = db.Table('likes',
                 db.Column('user_id', db.Integer,
                           db.ForeignKey('user.id'), primary_key=True),
                 db.Column('post_id', db.Integer,
                           db.ForeignKey('post.id'), primary_key=True))


# DB Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    # one to many relationship
    posts = db.relationship('Post', backref='user')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=True)
    likes = db.relationship('user', secondary=likes, backref='liked_posts')


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    posts = db.relationship('group', backref='group')
    users = db.relationship('user', secondary=groups, backref='groups')
