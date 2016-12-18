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
from ..models import UserModel
from .forms import LoginForm, JoinForm, ChangePasswordForm, PasswordResetForm, \
                   PasswordResetRequestForm, ChangeEmailForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        obj = UserModel.query.filter_by(email=email).first()
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
        # create new row and store in db
        user = UserModel(phone=form.phone.data, email=form.email.data,
                       password=form.password.data, state=True,
                       expire=datetime.today()+timedelta(days=365*10),
                       name=form.name.data, is_male=form.gender.data is 'M',
                       company=form.company.data,job=form.job.data,
                       address=form.address.data, qq=form.qq.data)
        db.session.add(user)
        db.session.commit()

        # add user to session
        login_user(user, False)

        # send confirmation email to user
        token = user.generate_confirmation_token()
        async_send_email(user.email, 'Confirm Your Account',
                         'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has sent to you by email')

        # remind admin
        name = form.name.data
        async_send_email(current_app.config['DEMO_MAIL_ADMIN'], 'new user: %s'%name, 'mail/new_user', name=name)

        return redirect(url_for('main.index'))

    # 'GET'
    return render_template('auth/join.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))

    if current_user.confirm(token):
        flash('You have confirmed your account.')
    else:
        flash('The confirmation link is invalid or expired.')
    return redirect(url_for('main.index'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    async_send_email(current_user.email, 'Confirm Your Account',
                     'auth/email/confirm', user=current_user, token=token)
    flash('A confirmation email has sent to you by email')
    return redirect(url_for('main.index'))

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.oldpassword.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Your password has been updated successfully!')
            return redirect(url_for('main.index'))
        else:
            flash("Invalid password.")
    return render_template('auth/change_password.html', form=form)


# protect un-confirmed user from accessing pages except "auth" views or "static"
@auth.before_app_request # before_request only impact request within blueprint
def before_request():
    if current_user.is_authenticated \
       and not current_user.confirmed \
       and request.endpoint[:5] != 'auth.'\
       and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/reset', methods=['GET','POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        # if validated, user must exists
        user = UserModel.query.filter_by(email=form.email.data).first()
        token = user.generate_reset_token()
        async_send_email(user.email, 'Reset Your Password',
                         'auth/email/reset_password', user=user,
                         token=token, next=request.args.get('next'))
        flash('An emmail with instruction to reset password has been sent to you.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if UserModel.reset_password(token, form.password.data):
            flash('Your password has been reset')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)

@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            async_send_email(new_email, 'Change Email Address',
                             'auth/email/change_email', user=current_user,
                             token=token)
            flash('An emmail with instruction to change email address has been sent to you.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password!')
    return render_template('auth/change_email.html', form=form)

@auth.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash("Your E-mail address has been changed")
    else:
        flash("Invalid request")
    return redirect(url_for("main.index"))




