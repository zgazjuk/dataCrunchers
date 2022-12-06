from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import Length, DataRequired, EqualTo, Email, Regexp
from wtforms import ValidationError
from models import User
from database import db


class RegisterForm(FlaskForm):
    class Meta:
        csrf = False

    firstname = StringField('First Name', validators=[Length(1, 20)])

    lastname = StringField('Last Name', validators=[Length(1, 20)])

    email = StringField('Email', [
        Email(message='Not a valid email address.'),
        DataRequired()])

    password = PasswordField('Password', [
        DataRequired(message="Please enter a password."),
        EqualTo('confirmPassword', message='Passwords must match')
    ])

    confirmPassword = PasswordField('Confirm Password', validators=[
        Length(min=6, max=20)
    ])

    submit = SubmitField('Sign Up')

    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).count() != 0:
            raise ValidationError('Email already in use.')


class LoginForm(FlaskForm):
    class Meta:
        csrf = False

    email = StringField('Email', [
        Email(message='Not a valid email address.'),
        DataRequired()])

    password = PasswordField('Password', [
        DataRequired(message="Please enter a password.")])

    submit = SubmitField('Login')

    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).count() == 0:
            raise ValidationError('Incorrect username or password.')

class NewTaskForm(FlaskForm):
    class Meta:
        csrf = False

    task_title = StringField('Title', validators=[Regexp('/^.{6,}$/', message="Title must be at least 6 characters and cannot only be whitespace."),
                                                Length(max=60),DataRequired('Required')])
    task_details = StringField('Title', validators=[Regexp('/^.{10,}$/', message="Title must be at least 10 characters and cannot only be whitespace."),
                                                Length(max=1000),DataRequired('Required')])

class CommentForm(FlaskForm):
    class Meta:
        csrf = False

    comment = TextAreaField('New Comment:', validators=[Length(min=1, max=256)])

    submit = SubmitField('Submit New Comment')

class SearchForm(FlaskForm):
    class Meta:
        csrf = False

    search = StringField('search')
