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
    SECRET_KEY = 'hard to guess string'

    # database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True # suppress annoying warn

    # mail
    MAIL_SERVER = 'smtp.sina.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # debug
    DEBUG = False

    # testing
    TESTING = False


class ProductConfig(BaseConfig):
    '''Configuration used in production environment.'''

    # security
    SECRET_KEY = 'hard to guess string'   # TODO

    # databse
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'product_data.sqlite')

    # mail
    MAIL_SERVER = ''                      # TODO


class DevelopConfig(BaseConfig):
    '''Configuration used in development environment.'''

    # debug
    DEBUG = True

class TestConfig(BaseConfig):
    '''Configuration used in test environment.'''

    # test
    TESTING = True
