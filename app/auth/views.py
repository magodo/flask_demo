#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#########################################################################
# Author: Zhaoting Weng
# Created Time: Tue 13 Dec 2016 11:04:56 PM CST
# Description:
#########################################################################

from datetime import datetime, timedelta
from flask import render_template, redirect, request, url_for, flash, current_app
from flask_login import login_user, login_required, logout_user, current_user

from .. import db
from . import auth
from ..email import async_send_email
from ..models import InfoModel
from .forms import LoginForm, JoinForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        obj = InfoModel.query.filter_by(email=email).first()
        if obj is not None and obj.verify_password(password):
            # add user to session
            login_user(obj, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('Invalid username or password!')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    # change online state to false
    current_user.state = False
    db.session.add(current_user)

    # pop user from session
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth.route('/join', methods=['GET','POST'])
def join():
    form = JoinForm()
    if form.validate_on_submit():
        name = form.name.data
        obj = InfoModel.query.filter_by(name=name).first()
        if obj is None:
            # create new row and store in db
            new_obj = InfoModel(phone=form.phone.data, email=form.email.data,
                           password=form.passwd.data, state=True,
                           expire=datetime.today()+timedelta(days=365*10),
                           name=form.name.data, is_male=form.gender.data is 'M',
                           company=form.company.data,job=form.job.data,
                           address=form.address.data, qq=form.qq.data)
            db.session.add(new_obj)

            # add user to session
            login_user(new_obj, False)

            # remind admin
            async_send_email(current_app.config['DEMO_MAIL_ADMIN'], 'new user: %s'%name, 'mail/new_user', name=name)

            return redirect(url_for('main.index'))
        else:
            flash('Name: "%s" has been used!'%name)
    # 'GET'
    return render_template('join.html', form=form)
