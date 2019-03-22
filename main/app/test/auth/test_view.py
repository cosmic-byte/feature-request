import unittest

from flask import url_for

from app import db
from app.auth.model import User
from app.test.base import BaseTestCase


def create_test_user():
    user = User(email='test@gmail.com', first_name='susan', last_name='daniel', password='mum')
    db.session.add(user)
    db.session.commit()
    return user


class TestAuthView(BaseTestCase):
    def test_user_login(self):
        """ Test for user login."""
        with self.client as client:
            user = create_test_user()

            url = url_for('auth.login')
            response = client.post(url, data=dict(email=user.email, password='mum'))
            self.assertRedirects(response, url_for('home.home'))

    def test_user_logout(self):
        """ Test for user logout."""
        with self.client as client:
            user = create_test_user()

            # Login user
            url = url_for('auth.login')
            response = client.post(url, data=dict(email=user.email, password='mum'))
            self.assertRedirects(response, url_for('home.home'))

            # Logout user
            logout_url = url_for('auth.logout')
            response = client.get(logout_url)
            self.assertRedirects(response, url_for('auth.login'))

            # Assess login required view should fail
            response = client.get(url_for('home.home'))
            self.assertRedirects(response, '{}{}'.format(url_for('auth.login'), '?next=%2F'))


if __name__ == '__main__':
    unittest.main()
