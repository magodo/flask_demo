from . import db

class InfoModel(db.Model):
    __tablename__ = 'infos'

    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String, unique=False, index=False, nullable=True, default=None)
    mail = db.Column(db.String, unique=False, index=False, nullable=True, default=None)
    passwd = db.Column(db.String, unique=False, index=False, nullable=False, default="")
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

