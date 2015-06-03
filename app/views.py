from flask import render_template, flash, redirect 
from .forms import LoginForm
from app import app

@app.route('/')
@app.route('/home')
def index():
    return render_template("base.html")

@app.route('/login',methods=['GET','POST'])
def sign_in():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for user: %s pass: %s ' % (form.username.data, form.password.data) )
		return redirect('/')
	return render_template("login.html", form=form)