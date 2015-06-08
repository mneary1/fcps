from flask.ext.wtf import Form
from flask.ext.wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app import app

class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])

class UploadForm(Form):
	upload = FileField('File to be uploaded', validators=[FileRequired(),FileAllowed(app.config['ALLOWED_EXTENSIONS'],"not allowed")])
	submit = SubmitField("Upload")

