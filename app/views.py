from flask import redirect, render_template
from app import app, admin
from app.models import db, User, Post, Group, groups, likes
from flask_admin.contrib.sqla import ModelView


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Group, db.session))

@app.route('/users/<id>.html')
def show_wall(id):
    user = User.one_or_404(id=id)
    return render_template('user_wall.html', user=user)