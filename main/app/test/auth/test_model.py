import unittest

from app import flask_bcrypt, db
from app.auth.model import User
from app.test.base import BaseTestCase
from app.util import save_changes


class TestAuthModels(BaseTestCase):

    def test_create(self):
        user1 = User(email='test1@gmail.com', first_name='susan', last_name='daniel', password='mum')
        user2 = User(email='test2@gmail.com', first_name='susan', last_name='daniel', password='mum')
        user3 = User(email='test3@gmail.com', first_name='susan', last_name='daniel', password='mum')

        db.session.add_all([user1, user2, user3])
        save_changes(db.session)

        users = User.query.all()
        self.assertEqual(len(users), 3)

    def test_password_hashing(self):
        user = User(email='test@gmail.com', first_name='susan', last_name='daniel', password='mum')
        self.assertFalse(user.password == 'mum')
        self.assertTrue(flask_bcrypt.check_password_hash(user.password, 'mum'))


if __name__ == '__main__':
    unittest.main()
