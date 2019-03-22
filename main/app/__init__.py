from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf import CSRFProtect

from .config import config_by_name

db = SQLAlchemy()
flask_bcrypt = Bcrypt()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    return app
