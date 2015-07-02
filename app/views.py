from flask import render_template, flash, redirect, session, url_for, request, send_from_directory, abort
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
        flash("You're already logged in, " + current_user.username + "!")
        return redirect('/')
    
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data, password=form.password.data).first()

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
 
    if request.method == 'POST':
        filename = secure_filename(form.upload.data.filename)
        if filename and "." in filename:
            ext = filename.split(".")[1]
            if ext not in app.config["ALLOWED_EXTENSIONS"]:
                flash("file extension ." + ext + " is not a supported upload type", "error")
                return redirect("/upload")
            full_path = os.path.join(app.config['UPLOAD_PATH'],current_user.username)

            #make the user's upload directory if it doesn't exist
            if not os.path.exists(full_path):
                os.makedirs(full_path)

            full_path = os.path.join(full_path, filename)
            form.upload.data.save(full_path)
            flash("successfully uploaded " + filename, "success")
            return redirect("/")
        else:
            flash("no file chosen","error")
            return redirect("/upload")
    
    return render_template("upload.html",form=form)

@app.route("/readings/")
def readings():

    path = app.config["READINGS_PATH"]
    all_mandatory = os.listdir(os.path.join(path,"mandatory"))
    all_review = os.listdir(os.path.join(path,"review"))
    all_misc = os.listdir(os.path.join(path,"misc"))
    mandatory = []
    review = []
    misc = []

    for reading in all_mandatory:
        if os.path.isfile(os.path.join(path,"mandatory",reading)):
                    mandatory.append(reading)
    mandatory.sort()

    for reading in all_review:
        if os.path.isfile(os.path.join(path,"review",reading)):
            review.append(reading)
    review.sort()

    for reading in all_misc:
        if os.path.isfile(os.path.join(path,"misc",reading)):
            misc.append(reading)
    misc.sort()

    return render_template("readings.html", mandatory=mandatory, review=review, misc=misc)

#serves up a specific reading requested
@app.route("/readings/<type>/<path:reading>")
def send_reading(reading, type):
    path = os.path.join(app.config["READINGS_PATH"],type)
    if os.path.exists(path):
        return send_from_directory(path, reading)
    return abort(404)

@app.route("/assignments/")
def assignments():
    path = app.config["ASSIGNMENTS_PATH"]
    all_programs = os.listdir(os.path.join(path, "programs"))
    all_activities = os.listdir(os.path.join(path, "activities"))
    programs = []
    activities = []

    for program in all_programs:
        if os.path.isfile(os.path.join(path, "programs", program)):
            programs.append(program)
    programs.sort()

    for activity in all_activities:
        if os.path.isfile(os.path.join(path, "activities", activity)):
            activities.append(activity)
    activities.sort()

    return render_template("assignments.html", programs=programs, activities=activities)

@app.route("/assignments/<type>/<path:assignment>")
def send_assignment(assignment, type):
    path = os.path.join(app.config["ASSIGNMENTS_PATH"],type)
    if os.path.exists(path):
        return send_from_directory(path,assignment)
    return abort(404)

''' error handlers '''
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(error):
    return "Something bad happened and you should tell Michael to look into it"

