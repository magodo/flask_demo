from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from . import login_manager
from . import db

class UserModel(UserMixin, db.Model):

    __tablename__ = 'infos'

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

    # TODO
    #def __repr__(self):
    #    return ""

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

@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))

