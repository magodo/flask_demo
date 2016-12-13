from datetime import datetime, timedelta
from flask import render_template, session, redirect, url_for, flash, current_app

from . import main
from .. import db
from .forms import LoginForm, JoinForm, ProfileForm
from ..models import InfoModel
from ..email import async_send_email

@main.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # 'POST'
        name = form.name.data
        passwd = form.passwd.data
        obj = InfoModel.query.filter_by(name=name).first()
        if not obj:
            flash('User "%s" not exists!'%name)
            return redirect(url_for(".login"))
        elif not obj.verify_password(passwd):
            flash('"User Name" or "Password" incorrect!')
            return redirect(url_for(".login"))
        else:
            # change online state
            obj.state = True
            db.session.add(obj)
            # store 'name' to session
            session['name'] = name
            return redirect(url_for('.index'))
    # 'GET'
    return render_template('login.html', form=form)

@main.route('/join', methods=['GET','POST'])
def join():
    form = JoinForm()
    if form.validate_on_submit():
        # 'POST'
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

            # store 'name' to session
            session['name'] = name

            # remind admin
            async_send_email(current_app.config['DEMO_MAIL_ADMIN'], 'new user: %s'%name, 'mail/new_user', name=name)

            return redirect(url_for('.index'))
        else:
            flash('Name: "%s" has been used!'%name)
            return redirect(url_for('.join'))
    # 'GET'
    return render_template('join.html', form=form)

@main.route('/logout', methods=['GET'])
def logout():
    # change online state to false
    user = InfoModel.query.filter_by(name=session['name']).first()
    user.state = False
    db.session.add(user)
    # pop 'user' from session
    session.pop('name')

    return redirect(url_for('.index'))

@main.route('/profile', methods=['GET', 'POST'])
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        # 'POST'
        # TODO: update db, show the current values for each field
        flash("Profile updated successfully!")
        return redirect(url_for('.profile'))
    # 'GET'
    return render_template('profile.html', form=form)
