import datetime

import uuid

from flask_login import UserMixin
from sqlalchemy_utils import UUIDType

from app import db, flask_bcrypt


class User(db.Model, UserMixin):
    """ User Model for storing user related details """
    __tablename__ = "auth_user"

    id = db.Column(UUIDType(binary=False), primary_key=True, unique=True, default=uuid.uuid4)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    authenticated = db.Column(db.Boolean, default=False)
    deleted = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, first_name, last_name, password, admin=False):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = flask_bcrypt.generate_password_hash(password).decode('utf-8')
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def __repr__(self):
        return '{}_{}'.format(self.shortened_id, self.first_name)

    @property
    def shortened_id(self):
        """Get shortened version of id."""
        return str(self.id)[-8:]
