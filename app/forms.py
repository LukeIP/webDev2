from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, NumberRange, Email, ValidationError, EqualTo
from app.models import User


class RegisterForm(FlaskForm):
    # ensuring that multiple usernames can't be created by one email
    def EmailExists(form, field):
        if User.query.filter_by(email=field.data.strip()).first() is not None:
            raise ValidationError("Account already associated with email")
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email(), EmailExists])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class PostForm(FlaskForm):
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Submit")

class AddGroupForm(FlaskForm):
    name = StringField("Group", validators=[DataRequired()])
    submit = SubmitField("Submit")

class AddUserGroupForm(FlaskForm):
    user = SelectField("User")
    submit = SubmitField("Submit")