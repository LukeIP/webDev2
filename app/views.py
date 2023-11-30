from flask import redirect, render_template
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_user
from app import app, admin, login_manager
from app.models import db, User, Post, Group, groups, likes
from .forms import LoginForm, RegisterForm

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Group, db.session))

# callback function to reload user object in session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/users/<id>')
def show_wall(id):
    user = User.query.filter_by(id=id).one_or_404(
        decription=f"No user with id '{id}'"
    )
    print(user.name)
    return render_template('user_wall.html', user=user)

@app.route("/register", methods=["GET", "POST"])
def register():
    # if user is already logged in then go to home page
    if current_user.is_authenticated:
        return redirect('/home')
    form = RegisterForm()
    if form.validate_on_submit():
        u = User(email=form.email.data.strip(), 
                 name=form.name.data.strip(),)
        u.set_password(form.password.data)
        db.session.add(u)
        db.session.commit()
        return redirect('/login')
    return render_template("register.html",form=form)

@app.route("/login", methods=["GET","POST"])
def login():
    # if user is already logegd in then go to home page
    if current_user.is_authenticated:
        return redirect('/home')
    form = LoginForm()
    if form.validate_on_submit():
        # login user
        u = User.query.filter_by(email=form.email.data.strip()).first()
        if u is not None and u.check_password(form.password.data):
            login_user(u, remember=True)
            return redirect('/home')
        else:
            return redirect('/login')   
    return render_template("login.html", form=form)