VirtualEnv
=========

The virtualenv of this project is created for **python2.7** with following command:

    # virtualenv -p /usr/bin/python2.7 venv    


Start Server
============

1. Start environment variables

    * `MAIL_USERNAM`: sender user name of mail(which is running SMTP server)
    * `MAIL_PASSOWRD`: sender password of mail
    * `DEMO_MAIL_SENDER`: sender mail, with form: *Foo bar <foobar@example.com>*
    * `DEMO_MAIL_ADMIN`: admin's email address
    * `SECRET_KEY`: secret key
    * (opt) `FLASK_CONFIG`: one of "developement", "testing", "production", "default"
    * (opt) `DEV_DATABASE_URL`: database url for development purpose
    * (opt) `TEST_DATABASE_URL`: database url for test purpose
    * (opt) `DATABASE_URL`: database url for production purpose

2. Run `./manager.py runserver`

Before Production
=================

1. Change `Demo` in every file to another name reflecting this project
2. Change *config.py* the `MAIL_SERVER` for class `ProductConfig`

TBD
===

See this [page](https://github.com/magodo/flask_demo/wiki/Requirement-Verification)

