#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#########################################################################
# Author: Zhaoting Weng
# Created Time: Tue 13 Dec 2016 11:37:09 PM CST
# Description:
#########################################################################

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,SelectField
from wtforms.validators import Required, Length, Email, Optional

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1,64),
                                             Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class JoinForm(FlaskForm):

    # mandatory
    name = StringField("Name", validators=[Length(1,6,"Length should be <= 6")])
    passwd = PasswordField("Passowrd", validators=[Required()])
    email = StringField("E-mail", validators=[Required(), Email("Invalid E-mail address")])

    # optional
    phone = StringField("Phone Number", validators = [Optional(), Length(11, 11, "Invalid phone number")])
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
