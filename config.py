#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#########################################################################
# Author: Zhaoting Weng
# Created Time: Mon 12 Dec 2016 07:41:11 PM CST
# Description: Default configuration. Only UPPERCASE variables will be loaded
#########################################################################

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
    '''Basic configuration class, to be inheritanted.'''

    # security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    # database
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True # suppress annoying warn

    # mail
    MAIL_SERVER = 'smtp.sina.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    DEMO_MAIL_SUBJECT_PREFIX = '[DEMO]'
    DEMO_MAIL_SENDER = os.environ.get('DEMO_MAIL_SENDER') or \
            'DEMO Admin <demo@example.com>'
    DEMO_MAIL_ADMIN = os.environ.get('DEMO_MAIL_ADMIN')

    # debug
    DEBUG = False

    # testing
    TESTING = False

    @staticmethod
    def init_app(app):
        pass


class ProductConfig(BaseConfig):
    '''Configuration used in production environment.'''

    # databse
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    # mail
    MAIL_SERVER = ''                      # TODO


class DevelopConfig(BaseConfig):
    '''Configuration used in development environment.'''

    # database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

    # debug
    DEBUG = True

class TestConfig(BaseConfig):
    '''Configuration used in test environment.'''

    # database
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

    # test
    TESTING = True

config = {
        'development': DevelopConfig,
        'testing': TestConfig,
        'production': ProductConfig,

        'default': DevelopConfig
}
