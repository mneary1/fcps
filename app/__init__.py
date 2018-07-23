from flask import Flask 
from flask_login import LoginManager 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

lm = LoginManager()
lm.login_view = "login"
lm.init_app(app)

from app import views, models
