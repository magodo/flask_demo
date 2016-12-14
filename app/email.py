import os
from threading import Thread
from flask import render_template, current_app
from flask_mail import Message

from . import mail

def async_send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object() # need the real object since it will be used in thread
    msg = Message(app.config['DEMO_MAIL_SUBJECT_PREFIX']+subject,
                  sender = app.config['DEMO_MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=thr_send_email, args=[app, msg])
    thr.start()
    return thr

def thr_send_email(app, msg):
    # although we have pushed app context, but it won't affect the thread, use app_context explicitly here
    with app.app_context():
        try:
            mail.send(msg)
        except TypeError as e:
            print "[WARNING] send mail failed: email related environment variables are not set"

