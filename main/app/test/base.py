import datetime

from flask_testing import TestCase

from app import db
from app.auth.model import User
from app.home.model import Client, Feature
from main.manage import app


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object('app.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


def get_user(email: str, password: str):
    user = User(
        email=email,
        first_name='Admin',
        last_name='Admin',
        password=password
    )
    db.session.add(user)
    db.session.commit()
    return user


def get_client(name: str) -> Client:
    client = Client(name=name)
    db.session.add(client)
    db.session.commit()
    return client


def get_feature_request(title: str, client: Client, user: User, priority: int):
    feature = Feature(
        title=title,
        description='Platform users should have 2nd factor authentication',
        client=str(client.id),
        requested_by=str(user.id),
        client_priority=priority,
        target_date=datetime.date(2019, 8, 8),
        product_area=Feature.PRODUCT_AREA_POLICIES
    )
    db.session.add(feature)
    db.session.commit()
    return feature
