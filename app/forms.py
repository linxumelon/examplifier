from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, validators
from wtforms.validators import DataRequired, InputRequired, ValidationError, EqualTo
from app.models import User

IDENTITY_CHOICES = [(1,"Student"),(2,"Instructor")]

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class UploadTestFileForm(FlaskForm):
    modcode = StringField('Module Code', validators=[DataRequired()])
    testfile = FileField(validators=[FileRequired('File was empty!')])
    submit = SubmitField('Upload')

class AddModuleForm(FlaskForm):
    modcode = StringField('Modcode', validators=[DataRequired()])
    submit = SubmitField('Add')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    id = StringField('Id', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    identity = SelectField('Identity', choices=IDENTITY_CHOICES, validators=[InputRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

    def validate_id(self, id):
        user = User.query.filter_by(id=id.data).first()
        if user is not None:
            raise ValidationError('This ID has been registered! Please login using your account.')