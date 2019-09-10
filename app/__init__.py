from flask import Flask 
from flask_login import LoginManager 
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin 

app = Flask(__name__)
app.config.from_object('config')
admin = Admin(app, name='CTY FCPS Admin Panel', template_mode='bootstrap3')

db = SQLAlchemy(app)

lm = LoginManager()
lm.login_view = "login"
lm.init_app(app)

from app import views, models
