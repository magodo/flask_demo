Dependency
=========

1. `flask-script`
2. `flask-bootstrap`
3. `flask-moment`
4. `flask-wtf`
5. `flask-sqlalchemy`
6. `flask-migrate`
7. `flask-mail`


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

1. 数据库模型中的`state`的具体含义
2. 
