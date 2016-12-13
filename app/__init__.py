from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

def create_app(config_name):
    # create app and push app context so that we always have an app context("current_app" == "app")
    app = Flask(__name__)
    app.app_context().push()

    # load config
    app.config.from_object(config[config_name])
    config[config_name].init_app(app) # currently do nothing


    # bind to app (each instance below could bind to more than one app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    # register blueprint
    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth') # every route defined via auth blueprint
                                                                # will have a prefix: '/login' -> 'auth/login'
    return app
