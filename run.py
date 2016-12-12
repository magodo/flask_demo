#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#########################################################################
# Author: Zhaoting Weng
# Created Time: Fri 09 Dec 2016 11:35:20 PM CST
# Description:
#########################################################################

import os
from datetime import datetime, timedelta

from flask import Flask, render_template, session, redirect, url_for, flash
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, PasswordField, SelectField, SelectMultipleField
from wtforms.validators import Required, Length, Email, Optional
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

basedir = os.path.abspath(os.path.dirname(__file__))

# create application
app = Flask(__name__)

# load default configuration
app.config.from_object('default_config.DevelopConfig')
# load configuration from environment variable to override the defaults
app.config.from_envvar("DEMO_CONFIGURATION", silent=True)

# create other global objects
db = SQLAlchemy(app)        # database
manager = Manager(app)      # CLI support
bootstrap = Bootstrap(app)  # bootstrap template
moment = Moment(app)        # time
migrate = Migrate(app, db)  # migrate db

# Shell "make_context" callback
def cb_make_context():
    return dict(app=app, db=db, TableInfo= TableInfo)
manager.add_command("shell", Shell(make_context=cb_make_context))
manager.add_command('db', MigrateCommand)

##########################
# Views
##########################

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # form is loaded automatically, `validate_on_submit()` will validate if current request is a "POST" and if it matches the rule defined in "form"
    if form.validate_on_submit():
        # 'POST'
        name = form.name.data
        passwd = form.passwd.data
        obj = TableInfo.query.filter_by(name=name).first()
        if not obj:
            flash('User "%s" not exists!'%name)
            return redirect(url_for("login"))
        elif obj.passwd != passwd:
            flash('"User Name" or "Password" incorrect!')
            return redirect(url_for("login"))
        else:
            # change online state
            obj.state = True
            db.session.add(obj)
            # store 'name' to session
            session['name'] = obj.name
            return redirect(url_for('index'))
    # 'GET'
    return render_template('login.html', form = form)

@app.route('/join/', methods=['GET','POST'])
def join():
    form = JoinForm()
    if form.validate_on_submit():
        # 'POST'
        obj = TableInfo.query.filter_by(name=form.name.data).first()
        if obj is None:
            new_obj = TableInfo(phone=form.phone.data, mail=form.mail.data,
                           passwd=form.passwd.data, state=True,
                           expire=datetime.today()+timedelta(days=365*10),
                           name=form.name.data, is_male=form.gender.data is 'M',
                           company=form.company.data,job=form.job.data,
                           address=form.address.data, qq=form.qq.data)
            db.session.add(new_obj)
            # store 'name' to session
            session['name'] = new_obj.name
            return redirect(url_for('index'))
        else:
            flash('Name: "%s" has been used!'%form.name.data)
            return redirect(url_for('join'))
    # 'GET'
    return render_template('join.html', form=form)

@app.route('/logout/', methods=['GET'])
def logout():
    # change online state to false
    user = TableInfo.query.filter_by(name=session['name']).first()
    user.state = False
    db.session.add(user)
    # pop 'user' from session
    session.pop('name')

    return redirect(url_for('index'))

@app.route('/profile/', methods=['GET', 'POST'])
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        # 'POST'
        flash("Profile updated successfully!")
        return redirect(url_for('profile'))
    # 'GET'
    return render_template('profile.html', form=form)

##########################
# Database models
##########################

class TableInfo(db.Model):
    __tablename__ = 'infos'

    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String, unique=False, index=False, nullable=True, default=None)
    mail = db.Column(db.String, unique=False, index=False, nullable=True, default=None)
    passwd = db.Column(db.String, unique=False, index=False, nullable=False, default="")
    state = db.Column(db.Boolean, unique=False, index=False, nullable=False, default=False) # TODO: clarify the meaning of this column(offline/online?)
    expire = db.Column(db.DateTime, unique=False, index=False, nullable=False, default=None)
    name = db.Column(db.String, unique=True, index=False, nullable=False)
    is_male = db.Column(db.Boolean, unique=False, index=False, nullable=False, default=True)
    birthday = db.Column(db.Date, unique=False, index=False, nullable=True, default=None)
    company = db.Column(db.String, unique=False, index=False, nullable=True, default=None)
    job = db.Column(db.String, unique=False, index=False, nullable=True, default=None)
    address = db.Column(db.String, unique=False, index=False, nullable=True, default=None)
    qq = db.Column(db.String, unique=False, index=False, nullable=True, default=None)
    #proj_count = db.Column(db.Integer, unique=False, index=False, nullable=True, default=None)

    # TODO
    #def __repr__(self):
    #    return ""


##########################
# Forms
##########################

class LoginForm(FlaskForm):
    name = StringField("User Name", validators = [Required()])
    passwd = PasswordField("Password", validators = [Required()])
    submit = SubmitField("Submit")

class JoinForm(FlaskForm):

    # mandatory
    name = StringField("Name", validators=[Length(1,6,"Length should be <= 6")])
    passwd = PasswordField("Passowrd", validators=[Required()])

    # optional
    phone = StringField("Phone Number", validators = [Optional(), Length(11, 11, "Invalid phone number")])
    mail = StringField("E-mail", validators=[Optional(), Email("Invalid E-mail address")])
    gender = SelectField("Gender", choices=[('M', 'Male'), ('F', 'Female')])
    ##birthday = #TODO
    company = StringField("Company")
    job = SelectField("Job", choices=[('dev', 'Developer'), ('op', 'Operator')])
    address = StringField("Address")
    qq = StringField("QQ number")
    # TODO: check how to specify HTML "row" attribute to the select field when rendering
    #projs = SelectMultipleField("Project(s) involved", choices=[
    #    ('p1', 'Project 1'), ('p2', 'Project 2'), ('p3', 'Project 3')])
    submit = SubmitField("Submit")

class ProfileForm(FlaskForm):

    # mandatory
    name = StringField("Name", validators=[Length(1,6,"Length should be <= 6")])
    passwd = PasswordField("Passowrd", validators=[Required()])
    # optional
    phone = StringField("Phone Number", validators = [Optional(), Length(11, 11, "Invalid phone number")])
    mail = StringField("E-mail", validators=[Optional(), Email("Invalid E-mail address")])
    gender = SelectField("Gender", choices=[('M', 'Male'), ('F', 'Female')])
    ##birthday = #TODO
    company = StringField("Company")
    job = SelectField("Job", choices=[('dev', 'Developer'), ('op', 'Operator')])
    address = StringField("Address")
    qq = StringField("QQ number")
    # TODO: check how to specify HTML "row" attribute to the select field when rendering
    #projs = SelectMultipleField("Project(s) involved", choices=[
    #    ('p1', 'Project 1'), ('p2', 'Project 2'), ('p3', 'Project 3')])
    submit = SubmitField("Submit")


##########################
# MAIN
##########################

if __name__ == "__main__":
    db.create_all() # create database if not exists
    manager.run()
