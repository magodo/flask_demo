from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager

from . import db

class InfoModel(UserMixin, db.Model):

    __tablename__ = 'infos'

    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String, unique=False, index=False, nullable=True, default=None)
    email = db.Column(db.String, unique=False, index=False, nullable=True, default=None)

    # set via "password" property
    password_hash = db.Column(db.String, unique=False, index=False, nullable=False, default="")

    state = db.Column(db.Boolean, unique=False, index=False, nullable=False, default=False) # TODO: clarify the meaning of this column(offline/online?)
    expire = db.Column(db.DateTime, unique=False, index=False, nullable=False, default=None)
    name = db.Column(db.String, unique=True, index=False, nullable=False)
    is_male = db.Column(db.Boolean, unique=False, index=False, nullable=False, default=True)
    birthday = db.Column(db.Date, unique=False, index=False, nullable=True, default=None)
    company = db.Column(db.String, unique=False, index=False, nullable=True, default=None)
    job = db.Column(db.String, unique=False, index=False, nullable=True, default=None)
    address = db.Column(db.String, unique=False, index=False, nullable=True, default=None)
    qq = db.Column(db.String, unique=False, index=False, nullable=True, default=None)
    #proj_count = db.Column(db.Integer, unique=False, index=False, nullable=True, default=None)

    # TODO
    #def __repr__(self):
    #    return ""

    # password related
    @property
    def password(self):
        '''Write-only attribute to store password hash'''
        raise AttributeError("password is not a readable attribute")
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return InfoModel.query.get(int(user_id))

