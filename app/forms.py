from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

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

