from flask import render_template, flash, redirect, session, url_for, request, send_from_directory
from flask.ext.login import login_user, logout_user, current_user, login_required 
from app import app, db, lm
from werkzeug import secure_filename
from .forms import LoginForm, UploadForm
from .models import User

import os

''' routes '''
@app.route('/')
@app.route('/home/')
def index():
    return render_template("base.html")

@app.route('/login/',methods=['GET','POST'])
def login():
	form = LoginForm()

	if current_user.is_authenticated():
		flash("you're already logged in, " + current_user.username + "!")
		return redirect('/')
	
	if form.validate_on_submit():
		print('Login requested for user: %s pass: %s ' % (form.username.data, form.password.data) )
		user = User.query.filter_by(username = form.username.data, password=form.password.data).first()
		print(user)
		if user is not None:
			login_user(user)
			flash("Login successful!", "success")
		else:
			flash("Incorrect login credentials :(", "error")

		return redirect('/login')

	return render_template("login.html", form=form)


@app.route("/logout/")
@login_required
def logout():
	logout_user()
	flash("Logout successful!", 'success')
	return redirect('/')

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.route('/upload/',methods=['GET','POST'])
@login_required
def upload():
	form = UploadForm()
 
	if form.validate_on_submit():
		filename = secure_filename(form.upload.data.filename)
		full_path = os.path.join(app.config['UPLOAD_PATH'],current_user.username)

		#make the user's upload directory if it doesn't exist
		if not os.path.exists(full_path):
			os.makedirs(full_path)

		full_path = os.path.join(full_path, filename)
		form.upload.data.save(full_path)
		flash("successfully uploaded " + filename )
		return redirect("/")

	return render_template("upload.html",form=form)

@app.route("/readings/")
def readings():

	path = app.config["READINGS_PATH"]
	potential_readings = os.listdir(path)
	actual_readings = []

	for reading in potential_readings:
		if os.path.isfile(os.path.join(path,reading)):
                    actual_readings.append(reading)

        actual_readings.sort()

	return render_template("readings.html", readings=actual_readings)

#serves up a specific reading requested
@app.route("/readings/<path:reading>")
def send_reading(reading):
	return send_from_directory(app.config["READINGS_PATH"], reading)

''' error handlers '''
@app.errorhandler(404)
def page_not_found(error):
	return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(error):
	return "Something bad happened and you should tell Michael to look into it"

