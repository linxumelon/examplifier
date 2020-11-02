import os
import sys
from flask_login import current_user, login_user, login_required
from flask import render_template, flash, redirect, url_for, request
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from app import app
from app import db
from app.forms import LoginForm, UploadTestFileForm, AddModuleForm
from app.models import User, Module, Teaches, Takes, TestPaper, StudentSubmission
from sqlalchemy import and_, or_, not_

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}
BASEDIR = './'

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template("index.html", title='Home Page')


@app.route('/upload_test_file', methods=['GET', 'POST']) 
@login_required
def upload_test_file():
    form = UploadTestFileForm()
    print("heeelllooooo")
    if form.validate_on_submit():
        print("heyyyyyy!")
        modcode = secure_filename(form.modcode.data)
        teaches = Teaches.query.filter_by(modcode=modcode, instructor_id=current_user.id).first()
        if not teaches:
            flash("No teaching record for this module. \n Please add module first if you are teaching this module. ")
            return redirect(url_for('index'))
        testfile = form.testfile.data
        filename = secure_filename(form.filename.data)
        moddir = Module.query.filter_by(code=modcode).first().dir
        
        files_with_given_name = TestPaper.query.filter_by(modcode=modcode, name=filename).all()
        if (len(files_with_given_name) > 0):
            filename = filename + " ({})".format(len(files_with_given_name))
        print("filename= {}".format(filename))
        fileurl = os.path.join(moddir, filename)
        file_record = TestPaper(modcode=modcode, name=filename, fileurl=fileurl)
        db.session.add(file_record)
        db.session.commit()
        print("fileurl = {}".format(fileurl))
        testfile.save(fileurl)
        flash('File successfully uploaded')
        return redirect(url_for('index'))
    else:
        print("its not valid")
    return render_template("upload_test_file.html", title='Upload Test File', form=form)

@app.route('/add_module', methods=['GET', 'POST'])
@login_required
def create_module():
    form = AddModuleForm()
    if form.validate_on_submit():
        modcode = secure_filename(form.modcode.data)
        dir_path = os.path.join(BASEDIR, modcode)
        os.mkdir(dir_path)
        module = Module.query.filter_by(code=modcode).first()
        if module is None:
            module = Module(code=modcode, dir=dir_path)
            print("module = {}".format(module))
            db.session.add(module)
            db.session.commit()
        teaches = Teaches.query.filter_by(modcode=modcode, instructor_id=current_user.id).first()
        if teaches is None:
            teaches = Teaches(instructor_id=current_user.id, instructor_name=current_user.username, modcode=modcode)
            print("teaches = {}".format(teaches))
            db.session.add(teaches)
            db.session.commit()
        else:
            print("Teaches exists: {}".format(teaches))
        return redirect(url_for('index'))
    
    return render_template('add_module.html', title='Add Module', form=form)
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print("user has password hash: {}".format(user.password_hash))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

