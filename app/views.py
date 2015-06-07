from flask import render_template, flash, redirect, session, url_for, request
from flask.ext.login import login_user, logout_user, current_user, login_required 
from app import app, db, lm
from .forms import LoginForm
from .models import User

@app.route('/')
@app.route('/home')
def index():
    return render_template("base.html")

@app.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm()

	if current_user.is_authenticated():
		flash("you're already logged in, " + current_user.username + "!")
		return redirect('/')
	
	if form.validate_on_submit():
		print('Login requested for user: %s pass: %s ' % (form.username.data, form.password.data) )
		user = User.query.filter_by(username = form.username.data).first()

		if user is not None:
			login_user(user)
			flash("Login successful!")
		else:
			print("Can't login: user", form.username.data, "doesn't exist.")

		return redirect('/')

	return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
	logout_user()
	flash("logout successful")
	return redirect('/')

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))