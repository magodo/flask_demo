from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin

from . import login_manager
from . import db


#################################################

class Permission(object):
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0X08
    ADMINISTER = 0Xff

#################################################
# Model
#################################################

class RoleModel(db.Model):

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('UserModel', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (Permission.ADMINISTER, False)
        }
        for r in roles:
            role = RoleModel.query.filter_by(name=r).first()
            if role is None:
                role = RoleModel(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return "<%s %r>"%(self.__class__, self.name)

class UserModel(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String, unique=False, index=False, default=None)
    email = db.Column(db.String, unique=False, index=False, default=None)

    # set via "password" property
    password_hash = db.Column(db.String, unique=False, index=False, default="")

    state = db.Column(db.Boolean, unique=False, index=False, default=False) # TODO: clarify the meaning of this column(offline/online?)
    expire = db.Column(db.DateTime, unique=False, index=False, default=None)
    name = db.Column(db.String, unique=True, index=False)
    is_male = db.Column(db.Boolean, unique=False, index=False, default=True)
    birthday = db.Column(db.Date, unique=False, index=False, default=None)
    company = db.Column(db.String, unique=False, index=False, default=None)
    job = db.Column(db.String, unique=False, index=False, default=None)
    address = db.Column(db.String, unique=False, index=False, default=None)
    qq = db.Column(db.String, unique=False, index=False, default=None)
    #proj_count = db.Column(db.Integer, unique=False, index=False, default=None)

    confirmed = db.Column(db.Boolean, default=False) # whether registering user is confirmed

    # point to "id" column for model whoes __tablename__ is "roles"
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, **kwargs):
        super(UserModel, self).__init__(**kwargs)
        if self.email == current_app.config['DEMO_ADMIN']:
            self.role = RoleModel.query.filter_by(permissions=Permission.ADMINISTER).first()
        else:
            self.role = RoleModel.query.filter_by(default=True).first()

    def __repr__(self):
        return "<%s %r>"%(self.__class__, self.name)

    # password property
    @property
    def password(self):
        '''Write-only attribute to store password hash'''
        raise AttributeError("password is not a readable attribute")
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # register authentification
    def generate_confirmation_token(self, expiration=3600): # expiration unit is second
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    # reset password
    def generate_reset_token(self, expiration=3600): # expiration unit is second
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        uid = data.get('reset')
        user = UserModel.query.filter_by(id=uid).first()
        user.password = new_password
        db.session.add(user)
        return True

    # change email address
    def generate_email_change_token(self, new_email, expiration=3600): # expiration unit is second
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        self.email = data.get('email')
        db.session.add(self)
        return True

    # Permission checking
    def can(self, permissions):
        return self.role is not None and \
                (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

#################################################

# Overload anonymous_user

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymouseUser
#################################################


# required by "login_manager"
@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))

