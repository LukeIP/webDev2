from flask import redirect, render_template
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_user, logout_user, login_required
from app import app, admin, login_manager
from app.models import db, User, Post, Group
from .forms import LoginForm, RegisterForm, PostForm, AddGroupForm

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Group, db.session))

# callback function to reload user object in session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/users/<id>')
def show_wall(id):
    user = User.query.get_or_404(id, description=f"No User with id {id} found.")
    # if user is logged in and going to their wall
    # then redirect to where they can also post
    if current_user.is_authenticated and int(current_user.id) == int(id):
        return redirect('/home')
    return render_template("wall.html", name=user.name,
                           posts=user.posts)

@app.route("/group/<id>")
def group_wall(id):
    if current_user.is_authenticated and int(id) in current_user.groups:
        return redirect(f"/group_post/{id}")
    group = Group.query.get_or_404(id, description=f"No Group with id {id} found.")
    return render_template("wall.html", name=group.name,
                           post=group.posts)

@app.route("/group_post/<id>")
@login_required
def group_post_wall(id):
    if id not in current_user.groups:
        return redirect(f"/group/{id}")
    group = Group.query.get_or_404(id, description=f"No Group with id {id} found.")
    form = PostForm()
    if form.validate_on_submit():
        p = Post(text=form.content.data.strip(),
                 user_id=current_user.id,
                 group_id=id)
        db.session.add(p)
        db.session.commit()
        return redirect("/group_post/<id>") 
    return render_template("wall.html", name=group.name,
                           post=group.posts, form=form)
    

@app.route("/add_group", methods=["GET", "POST"])
@login_required
def add_group():
    form = AddGroupForm()
    if form.validate_on_submit():
        g=Group(name=form.name.data.strip(),
                owner_id = current_user.id)
        db.session.add(g)
        db.session.commit()
        return redirect(f"/group_post/{g.id}")
    return render_template("add_group.html", form=form)

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


@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    form = PostForm()
    if form.validate_on_submit():
        p = Post(text = form.content.data.strip(),
                 user_id = current_user.id)
        db.session.add(p)
        db.session.commit()
        return redirect("/home")
    posts = current_user.posts
    return render_template("home.html", user=current_user, form=form,
                           posts=posts, name="Wall")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect("/home")
    else:
        return redirect("/login")