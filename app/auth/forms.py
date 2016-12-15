#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#########################################################################
# Author: Zhaoting Weng
# Created Time: Tue 13 Dec 2016 11:37:09 PM CST
# Description:
#########################################################################

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,SelectField
from wtforms.validators import Required, Length, Email, Optional, Regexp, EqualTo, ValidationError

from ..models import UserModel

###################
# custom validators
###################

class UniqBase(object):
    '''Validator to ensure a field is not used in DB'''
    def __init__(self, model):
        self.model = model

class UniqName(UniqBase):
    '''User name uniqueness'''
    def __init__(self, model, message=None):
        super(UniqName, self).__init__(model)
        if not message:
            message = u'Username is already used!'
        self.message = message

    def __call__(self, form, field):
        user = self.model.query.filter_by(name=field.data).first()
        if user is not None:
            raise ValidationError(self.message)

class UniqEmail(UniqBase):
    '''email uniqueness'''
    def __init__(self, model, message=None):
        super(UniqEmail, self).__init__(model)
        if not message:
            message = u'Email is already used!'
        self.message = message

    def __call__(self, form, field):
        user = self.model.query.filter_by(email=field.data).first()
        if user is not None:
            raise ValidationError(self.message)

###################
# Forms
###################

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1,64),
                                             Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class JoinForm(FlaskForm):

    # mandatory
    email = StringField("E-mail", validators=[Required(), Length(1,64),
                         Email("Invalid E-mail address"), UniqEmail(UserModel)])
    name = StringField("Username", validators=[Required(), Length(1,6,
                        "User name should be less than 6 characters"),
                        Regexp('^[a-zA-Z][A-Za-z0-9_.]*$', 0, 'Username must have only letters, '
                        'numbers, dots or underscores and starts with letters.'), UniqName(UserModel)])
    password = PasswordField("Passowrd", validators=[Required(), EqualTo('password2', 'Passowrd must match!')])
    password2 = PasswordField("Confirm password", validators=[Required()])

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
    submit = SubmitField("Join")

class ChangePasswordForm(FlaskForm):
    oldpassword = PasswordField("Old Passowrd", validators=[Required()])
    password = PasswordField("New Passowrd", validators=[Required(), EqualTo('password2', 'Passowrd must match!')])
    password2 = PasswordField("Confirm New Password", validators=[Required()])
    submit = SubmitField("Update Passowrd")



