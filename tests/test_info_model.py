#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#########################################################################
# Author: Zhaoting Weng
# Created Time: Tue 13 Dec 2016 10:13:39 PM CST
# Description:
#########################################################################

import unittest
from app.models import InfoModel

class InfoModelTestCase(unittest.TestCase):

    def test_password_setter(self):
        i = InfoModel(password = 'cat')
        self.assertTrue(i.password_hash is not None)

    def test_no_password_getter(self):
        i = InfoModel(password = 'cat')
        with self.assertRaises(AttributeError):
            i.password

    def test_password_verification(self):
        i = InfoModel(password = 'cat')
        self.assertTrue(i.verify_password('cat'))
        self.assertFalse(i.verify_password('dog'))

    def test_password_salts_are_random(self):
        i1 = InfoModel(password = 'cat')
        i2 = InfoModel(password = 'cat')
        self.assertTrue(i1.password_hash != i2.password_hash)



