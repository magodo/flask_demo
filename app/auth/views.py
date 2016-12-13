#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#########################################################################
# Author: Zhaoting Weng
# Created Time: Tue 13 Dec 2016 11:04:56 PM CST
# Description:
#########################################################################

from flask import render_template

from . import auth

@auth.route('/login')
def login():
    return render_template('auth/login.html')

