from flask_wtf import Form
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, ValidationError
from app import app

class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField("Login")

class UploadForm(Form):
	upload = FileField('Upload a file:', validators=[FileRequired(),FileAllowed(app.config['ALLOWED_EXTENSIONS'],"not allowed")])
	submit = SubmitField("Upload")

