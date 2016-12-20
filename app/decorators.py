#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#########################################################################
# Author: Zhaoting Weng
# Created Time: Tue 20 Dec 2016 11:42:16 PM CST
# Description:
#########################################################################

from functools import wraps
from flask import abort
from flask_login import current_user

from .models import Permission

def permission_required(permission):
    def decorator(f):
        @wraps(f) # this is for retaining the metadata of the decorated func
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

admin_required = permission_required(Permission.ADMINISTRATOR)
