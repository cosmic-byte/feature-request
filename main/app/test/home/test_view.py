import datetime
import unittest

from flask import url_for

from app.home.forms import FeatureRequestForm
from app.home.model import Feature
from app.test.base import BaseTestCase, get_user, get_client, get_feature_request


class TestFeatureRequestViews(BaseTestCase):

    def login_user(self, user):
        url = url_for('auth.login')
        with self.client as client:
            client.post(url, data=dict(email=user.email, password='password'))
            return client

    def test_create_feature_request_success(self):
        """ Test create feature request."""
        user = get_user('admin@admin.com', 'password')
        client = self.login_user(user)

        request_client = get_client(name='Client A')

        feature_data = {
            'title': 'New Feature',
            'description': 'New Feature description',
            'client': str(request_client.id),
            'client_priority': 1,
            'target_date': datetime.date(2019, 8, 8),
            'product_area': Feature.PRODUCT_AREA_REPORTS
        }
        url = url_for('home.create_request')
        response = client.post(url, data=feature_data)
        self.assertRedirects(response, url_for('home.home'))

    def test_create_feature_request_for_same_client_with_repeated_priority_should_reorder_priorities(self):
        """ Test create feature request."""
        user = get_user('admin@admin.com', 'password')
        client = self.login_user(user)

        request_client = get_client(name='Client A')

        get_feature_request(title='Feature A', client=request_client, user=user, priority=1)
        get_feature_request(title='Feature B', client=request_client, user=user, priority=2)
        get_feature_request(title='Feature C', client=request_client, user=user, priority=3)
        get_feature_request(title='Feature D', client=request_client, user=user, priority=4)

        feature_data = {
            'title': 'Feature E',
            'description': 'New Feature description',
            'client': str(request_client.id),
            'client_priority': 2,
            'target_date': datetime.date(2019, 8, 8),
            'product_area': Feature.PRODUCT_AREA_REPORTS
        }
        url = url_for('home.create_request')
        response = client.post(url, data=feature_data)
        self.assertRedirects(response, url_for('home.home'))

        feature_a = Feature.query.filter_by(title='Feature A').first()
        feature_b = Feature.query.filter_by(title='Feature B').first()
        feature_c = Feature.query.filter_by(title='Feature C').first()
        feature_d = Feature.query.filter_by(title='Feature D').first()
        feature_e = Feature.query.filter_by(title='Feature E').first()

        self.assertEqual(feature_a.client_priority, 1)
        self.assertEqual(feature_b.client_priority, 3)
        self.assertEqual(feature_c.client_priority, 4)
        self.assertEqual(feature_d.client_priority, 5)
        self.assertEqual(feature_e.client_priority, 2)

    def test_create_feature_request_for_same_client_without_repeated_priority_should_not_reorder_priorities(self):
        """ Test create feature request."""
        user = get_user('admin@admin.com', 'password')
        client = self.login_user(user)

        request_client = get_client(name='Client A')

        get_feature_request(title='Feature A', client=request_client, user=user, priority=1)
        get_feature_request(title='Feature B', client=request_client, user=user, priority=2)
        get_feature_request(title='Feature C', client=request_client, user=user, priority=6)
        get_feature_request(title='Feature D', client=request_client, user=user, priority=7)

        feature_data = {
            'title': 'Feature E',
            'description': 'New Feature description',
            'client': str(request_client.id),
            'client_priority': 3,
            'target_date': datetime.date(2019, 8, 8),
            'product_area': Feature.PRODUCT_AREA_REPORTS
        }
        url = url_for('home.create_request')
        response = client.post(url, data=feature_data)
        self.assertRedirects(response, url_for('home.home'))

        feature_a = Feature.query.filter_by(title='Feature A').first()
        feature_b = Feature.query.filter_by(title='Feature B').first()
        feature_c = Feature.query.filter_by(title='Feature C').first()
        feature_d = Feature.query.filter_by(title='Feature D').first()
        feature_e = Feature.query.filter_by(title='Feature E').first()

        self.assertEqual(feature_a.client_priority, 1)
        self.assertEqual(feature_b.client_priority, 2)
        self.assertEqual(feature_c.client_priority, 6)
        self.assertEqual(feature_d.client_priority, 7)
        self.assertEqual(feature_e.client_priority, 3)

    def test_create_feature_request_for_different_clients_with_same_priority_should_not_reorder_priorities(self):
        """ Test create feature request."""
        user = get_user('admin@admin.com', 'password')
        client = self.login_user(user)

        request_client1 = get_client(name='Client A')
        request_client2 = get_client(name='Client B')
        request_client3 = get_client(name='Client C')
        request_client4 = get_client(name='Client D')

        get_feature_request(title='Feature A', client=request_client1, user=user, priority=1)
        get_feature_request(title='Feature A', client=request_client2, user=user, priority=1)
        get_feature_request(title='Feature A', client=request_client3, user=user, priority=1)

        feature_data = {
            'title': 'Feature A',
            'description': 'New Feature description',
            'client': str(request_client4.id),
            'client_priority': 1,
            'target_date': datetime.date(2019, 8, 8),
            'product_area': Feature.PRODUCT_AREA_REPORTS
        }
        url = url_for('home.create_request')
        response = client.post(url, data=feature_data)
        self.assertRedirects(response, url_for('home.home'))

        feature1 = Feature.query.filter_by(client=str(request_client1.id)).first()
        feature2 = Feature.query.filter_by(client=str(request_client2.id)).first()
        feature3 = Feature.query.filter_by(client=str(request_client3.id)).first()
        feature4 = Feature.query.filter_by(client=str(request_client4.id)).first()

        self.assertEqual(feature1.client_priority, 1)
        self.assertEqual(feature2.client_priority, 1)
        self.assertEqual(feature3.client_priority, 1)
        self.assertEqual(feature4.client_priority, 1)

    def test_get_user_feature_requests(self):
        """Get feature requests."""
        user = get_user('admin@admin.com', 'password')
        client = self.login_user(user)

        request_client = get_client(name='Client A')

        get_feature_request(title='Feature A', client=request_client, user=user, priority=1)
        get_feature_request(title='Feature A', client=request_client, user=user, priority=2)

        url = url_for('home.home')
        response = client.get(url)
        self.assert200(response)

    def test_edit_feature_request_success(self):
        """ Test edit feature request."""
        user = get_user('user@gmail.com', 'password')
        client = self.login_user(user)

        request_client = get_client(name='Client A')
        feature_request = get_feature_request(title='Feature A', client=request_client, user=user, priority=1)

        edit_data = FeatureRequestForm(obj=feature_request).data
        edit_data['description'] = 'This is a different description'

        url = url_for('home.edit_request', request_id=str(feature_request.id))
        response = client.patch(url, data=edit_data)
        self.assertRedirects(response, url_for('home.home'))

        feature_request_updated = Feature.query.get(str(feature_request.id))
        self.assertEqual(feature_request_updated.title, feature_request.title)
        self.assertEqual(feature_request_updated.description, edit_data['description'])
        self.assertEqual(feature_request_updated.client, feature_request.client)
        self.assertEqual(feature_request_updated.target_date, feature_request.target_date)

    def test_edit_feature_request_for_same_client_with_repeated_priority_should_reorder_priorities(self):
        """ Test create feature request."""
        user = get_user('admin@admin.com', 'password')
        client = self.login_user(user)

        request_client = get_client(name='Client A')

        get_feature_request(title='Feature A', client=request_client, user=user, priority=1)
        get_feature_request(title='Feature B', client=request_client, user=user, priority=2)
        get_feature_request(title='Feature C', client=request_client, user=user, priority=3)
        feature_request = get_feature_request(title='Feature D', client=request_client, user=user, priority=4)

        edit_data = FeatureRequestForm(obj=feature_request).data
        edit_data['description'] = 'This is a different description'
        edit_data['client_priority'] = 1

        url = url_for('home.edit_request', request_id=str(feature_request.id))
        response = client.patch(url, data=edit_data)
        self.assertRedirects(response, url_for('home.home'))

        feature_a = Feature.query.filter_by(title='Feature A').first()
        feature_b = Feature.query.filter_by(title='Feature B').first()
        feature_c = Feature.query.filter_by(title='Feature C').first()
        feature_d = Feature.query.filter_by(title='Feature D').first()

        self.assertEqual(feature_a.client_priority, 2)
        self.assertEqual(feature_b.client_priority, 3)
        self.assertEqual(feature_c.client_priority, 4)
        self.assertEqual(feature_d.client_priority, 1)

    def test_delete_feature_request_success(self):
        """ Test delete feature request."""
        user = get_user('user@gmail.com', 'password')
        client = self.login_user(user)

        request_client = get_client(name='Client A')
        feature_request = get_feature_request(title='Feature A', client=request_client, user=user, priority=1)

        self.assertEqual(feature_request.deleted, False)
        url = url_for('home.delete_request', request_id=str(feature_request.id))
        response = client.get(url)
        self.assertRedirects(response, url_for('home.home'))

        feature_request_updated = Feature.query.get(str(feature_request.id))
        self.assertEqual(feature_request_updated.deleted, True)


if __name__ == '__main__':
    unittest.main()
