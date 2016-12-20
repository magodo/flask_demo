#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#########################################################################
# Author: Zhaoting Weng
# Created Time: Mon 12 Dec 2016 10:44:58 PM CST
# Description:
#########################################################################

import os
from app import create_app, db
from app.models import UserModel, RoleModel
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def cb_make_context():
    return dict(app=app, db=db, UserModel=UserModel, RoleModel=RoleModel)
manager.add_command("shell", Shell(make_context=cb_make_context))
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    '''Run unit test.'''
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == "__main__":
    db.create_all(app=app)
    manager.run()
