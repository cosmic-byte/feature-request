import unittest

from app.home.model import Feature, Client
from app.test.base import BaseTestCase, get_client, get_feature_request, get_user


class TestHomeModels(BaseTestCase):

    def test_create(self):
        user = get_user(email='test1@gmail.com', password='password')

        client1 = get_client(name='Client A')
        client2 = get_client(name='Client B')
        get_client(name='Client C')

        get_feature_request(title='Feature A', client=client1, user=user, priority=1)
        get_feature_request(title='Feature B', client=client2, user=user, priority=2)

        clients = Client.query.all()
        requests = Feature.query.all()
        self.assertEqual(len(clients), 3)
        self.assertEqual(len(requests), 2)

        self.assertEqual(Feature.query.filter_by(client_priority=2).first().client, client2.id)
        self.assertEqual(Feature.query.filter_by(client_priority=1).first().client, client1.id)


if __name__ == '__main__':
    unittest.main()
