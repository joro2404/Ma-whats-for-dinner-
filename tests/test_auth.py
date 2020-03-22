import unittest


from tests.base import BaseTestCase


class FlaskTestCase(BaseTestCase):

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


    def test_login_page_loads(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)


    def test_profile_route_requires_login(self):
        response = self.client.get('/profile', follow_redirects=True)
        self.assertIn(b'Please log in to access this page.', response.data)


    def test_login_successful(self):
        response = self.client.post(
            '/login',
            data=dict(email="admin@admin.com", password="admin"),
            follow_redirects=True
        )
        self.assertIn(b'Hi admin!', response.data)


    def test_login_if_already_logged(self):
        self.client.post(
            '/login',
            data=dict(email="admin@admin.com", password="admin"),
            follow_redirects=True
        )
        response = self.client.post('/login', follow_redirects=True)
        self.assertIn(b'You are already logged in!', response.data)


    def test_login_unsuccessful(self):
        response = self.client.post(
            '/login',
            data=dict(email="admin@admin.com", password="wrong"),
            follow_redirects=True
        )
        self.assertIn(b'Please check your login credentials!', response.data)


    def test_register_email_already_existing(self):
        response = self.client.post(
            '/register',
            data=dict(
                email="admin@admin.com", 
                password="admin", 
                username="admin",
                sensor_id=76
            ),
            follow_redirects=True
        )
        self.assertIn(b'Email address already registered!', response.data)


    def test_register_sensor_already_existing(self):
        response = self.client.post(
            '/register',
            data=dict(
                email="test@admin.com", 
                password="admin", 
                username="admin",
                sensor_id=76
            ),
            follow_redirects=True
        )
        self.assertIn(b'Sensor already registered!', response.data)


if __name__ == '__main__':
    unittest.main()