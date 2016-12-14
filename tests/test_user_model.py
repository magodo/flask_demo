#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#########################################################################
# Author: Zhaoting Weng
# Created Time: Tue 13 Dec 2016 10:13:39 PM CST
# Description:
#########################################################################

import unittest
import time
from app import create_app, db
from app.models import UserModel

class UserModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        i = UserModel(password = 'cat')
        self.assertTrue(i.password_hash is not None)

    def test_no_password_getter(self):
        i = UserModel(password = 'cat')
        with self.assertRaises(AttributeError):
            i.password

    def test_password_verification(self):
        i = UserModel(password = 'cat')
        self.assertTrue(i.verify_password('cat'))
        self.assertFalse(i.verify_password('dog'))

    def test_password_salts_are_random(self):
        i1 = UserModel(password = 'cat')
        i2 = UserModel(password = 'cat')
        self.assertTrue(i1.password_hash != i2.password_hash)

    def test_valid_confirm_token(self):
        u = UserModel(password = 'cat')
        db.session.add(u)
        db.session.commit()
        # now 'id' is available so that to generate token
        s = u.generate_confirmation_token()
        self.assertTrue(u.confirm(s))

    def test_invalid_confirm_token(self):
        u1 = UserModel(password='cat')
        u2 = UserModel(password='dog')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        s1 = u1.generate_confirmation_token()
        self.assertFalse(u2.confirm(s1))

    def test_expire_confirm_token(self):
        u = UserModel(password = 'cat')
        db.session.add(u)
        db.session.commit()
        # now 'id' is available so that to generate token
        s = u.generate_confirmation_token(expiration=1)
        time.sleep(2)
        self.assertFalse(u.confirm(s))

