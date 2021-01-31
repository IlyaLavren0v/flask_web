from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from .models import User
from flask_wtf.file import FileField, FileAllowed

class UserRegisterForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    first_name  = StringField(label="First Name")
    last_Name = StringField(label="Last Name")
    age = StringField(label="Age")
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    password_comparison = PasswordField(label='Repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(label="Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("A user with this name already exists.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("A user with this email already exists")

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    rating = StringField("Rating", validators=[DataRequired()])
    picture = FileField('Upload the book cover', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Publication')

class JournalForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    editor = StringField("Editor", validators=[DataRequired()])
    page_amount = StringField("Number pages", validators=[DataRequired()])
    picture = FileField('Upload the journal cover', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Publication')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember =  BooleanField('Remember me?')
    submit = SubmitField('Log In')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    first_name  = StringField(label="First Name", validators=[DataRequired()])
    last_Name = StringField(label="Last Name", validators=[DataRequired()]) 
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField(label='Profile avatar', validators=[FileAllowed(['jpg', 'jpeg', 'svg', 'png'])])
    submit = SubmitField('Update')