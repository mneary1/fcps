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
            return redirect("/upload")
        else:
            flash("no file chosen","error")
            return redirect("/upload")
    
    uploads = get_files(app.config['UPLOAD_PATH'], current_user.username)
    return render_template("upload.html",form=form, uploads=uploads)

@app.route("/readings/")
def readings():
    path = app.config["READINGS_PATH"]
    mandatory = get_files(path, "mandatory")
    review = get_files(path, "review")
    misc = get_files(path, "misc")
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
    programs = get_files(path, "programs")
    activities = get_files(path, "activities")
    return render_template("assignments.html", programs=programs, activities=activities)

@app.route("/assignments/<type>/<path:assignment>")
def send_assignment(assignment, type):
    path = os.path.join(app.config["ASSIGNMENTS_PATH"],type)
    if os.path.exists(path):
        return send_from_directory(path,assignment)
    return abort(404)

@app.route("/references/")
def references():
    references = get_files(os.path.join(app.config["REFERENCES_PATH"]))
    return render_template("references.html", references=references)

@app.route("/references/<path:reference>")
def send_references(reference):
    if os.path.exists(app.config["REFERENCES_PATH"]):
        return send_from_directory(app.config["REFERENCES_PATH"],reference)
    return abort(404)

''' error handlers '''
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(error):
    return "Something bad happened and you should tell Michael to look into it"

'''helper functions'''
def get_files(base_path, child=''):
    full_path = os.path.join(base_path,child)

    if not os.path.exists(full_path):
        return []

    all_files = os.listdir(full_path)
    actual_files = []

    for potential_file in all_files:
        if os.path.isfile(os.path.join(full_path,potential_file)):
            actual_files.append(potential_file)

    actual_files.sort()
    return actual_files
