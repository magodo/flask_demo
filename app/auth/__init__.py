#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#########################################################################
# Author: Zhaoting Weng
# Created Time: Tue 13 Dec 2016 11:02:44 PM CST
# Description:
#########################################################################

from flask import Blueprint

auth = Blueprint('auth', '__main__')

from . import views
