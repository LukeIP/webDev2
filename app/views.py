from flask import redirect, render_template
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_user, logout_user, login_required
from app import app, admin, login_manager
from app.models import db, User, Post, Group
from .forms import LoginForm, RegisterForm, PostForm, AddGroupForm, AddUserGroupForm

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Group, db.session))

# callback function to reload user object in session


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/likes/<user_id>')
def show_likes(user_id):
    # get user or 404 with desc otherwise
    user = User.query.get_or_404(
        user_id, description=f"No User with id {id} found.")
    likes = user.liked_posts
    return render_template("show_like.html", title=f"{user.name} likes",
                           likes=likes, user=user)


@app.route('/users')
def show_users():
    return render_template(
        "table_elements.html",
        title="User",
        data=User.query.all())


@app.route('/groups')
def show_groups():
    return render_template(
        "table_elements.html",
        title="Group",
        data=Group.query.all())


@app.route('/User/<id>')
def show_wall(id):
    # get user or 404 with desc otherwise
    user = User.query.get_or_404(
        id, description=f"No User with id {id} found.")
    # if user is logged in and going to their wall
    # then redirect to where they can also post
    if current_user.is_authenticated and int(current_user.id) == int(id):
        return redirect('/home')
    return render_template("wall.html", name=user.name,
                           posts=user.posts, title=user.name,
                           curent_user=current_user)


@app.route('/like/<post_id>')
def like(post_id):
    # if user is logged in
    if current_user.is_authenticated:
        # add to liked posts
        p = Post.query.get(post_id)
        if current_user in p.likes:
            p.likes.remove(current_user)
        else:
            p.likes.append(current_user)
        db.session.commit()
    return "success"


@app.route("/Group/<id>")
def group_wall(id):
    # if user is logged in and in this group
    if current_user.is_authenticated and id in current_user.groups:
        # return higher privlege web page
        return redirect(f"/group_post/{id}")
    group = Group.query.get_or_404(
        id, description=f"No Group with id {id} found.")
    return render_template("wall.html", name=group.name,
                           posts=group.posts, title=group.name)


@app.route("/group_post/<id>", methods=["GET", "POST"])
@login_required
def group_post_wall(id):
    # if user isn't in this group then redirect to
    # lower privilege group wall
    if id not in current_user.groups:
        return redirect(f"/group/{id}")
    # get group or return 404 with that message if
    # not found
    group = Group.query.get_or_404(
        id, description=f"No Group with id {id} found.")
    form = PostForm()
    if form.validate_on_submit():
        p = Post(text=form.content.data.strip(),
                 user_id=current_user.id,
                 )
        db.session.add(p)
        db.session.commit()
        group.posts.append(p)
        db.session.commit()
        return redirect(f"/group_post/{id}")
    return render_template("group_post.html", name=group.name,
                           posts=group.posts, form=form,
                           title=group.name, id=group.id)


@app.route("/add_group_user/<id>", methods=["GET", "POST"])
@login_required
def add_group_user(id):
    # get all usesrs
    users = User.query.all()
    form = AddUserGroupForm()
    # convert all user emails to list and add to form
    email = []
    for user in users:
        email.append(user.email)
    form.user.choices = email
    if form.validate_on_submit():
        # filter user according to email then add user to group
        g = Group.query.get(id)
        u = user.query.filter_by(email=form.user.data).first()
        g.users.append(u)
        db.session.commit()
        return redirect(f"/Group/{id}")
    return render_template(
        "add_group_user.html",
        title="Add User to Group",
        form=form)


@app.route("/add_group", methods=["GET", "POST"])
@login_required
def add_group():
    form = AddGroupForm()
    if form.validate_on_submit():
        g = Group(name=form.name.data.strip(),
                  owner_id=current_user.id)
        # add user to group
        g.users.append(current_user)
        db.session.add(g)
        db.session.commit()
        return redirect(f"/group_post/{g.id}")
    return render_template("add_group.html", form=form,
                           title="Add Group")


@app.route("/register", methods=["GET", "POST"])
def register():
    # if user is already logged in then go to home page
    if current_user.is_authenticated:
        return redirect('/home')
    form = RegisterForm()
    # set user according to password hash
    if form.validate_on_submit():
        u = User(email=form.email.data.strip(),
                 name=form.name.data.strip(),)
        u.set_password(form.password.data)
        db.session.add(u)
        db.session.commit()
        return redirect('/login')
    return render_template("register.html", form=form,
                           title="Register")


@app.route("/login", methods=["GET", "POST"])
def login():
    # if user is already logeged in then go to home page
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
    return render_template("login.html", form=form,
                           title="Login")


@app.route("/home", methods=["GET", "POST"])
@login_required
def home():
    # home is user wall but iwht post privlileges
    form = PostForm()
    if form.validate_on_submit():
        # make post according to form data
        p = Post(text=form.content.data.strip(),
                 user_id=current_user.id)
        db.session.add(p)
        db.session.commit()
        return redirect("/home")
    posts = current_user.posts
    return render_template("home.html", user=current_user, form=form,
                           posts=posts, name="Wall", title="Home")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route("/")
def index():
    # redirect user to relevant page
    if current_user.is_authenticated:
        return redirect("/home")
    else:
        return redirect("/login")
