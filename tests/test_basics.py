#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#########################################################################
# Author: Zhaoting Weng
# Created Time: Tue 13 Dec 2016 12:21:48 AM CST
# Description:
#########################################################################

import unittest
from flask import current_app
from app import create_app, db

class BasicsTest(unittest.TestCase):

    def setUp(self):
        '''UT setup function.'''
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        '''UT teardown function.'''
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

