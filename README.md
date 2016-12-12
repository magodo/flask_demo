Start Server
============

1. Export `MAIL_USERNAME` and `MAIL_PASSWORD` environment variables
2. Run `./run.py runserver`

Before Production
=================

1. In *run.py*, change `DEMO_CONFIGURATION` to another name reflecting this project
2. In *templates/base.html*, change `Demo` to another name reflecting this project
3. Change *default_config.py* the `SECRET_KEY`, `MAIL_SERVER` for class `ProductConfig`
