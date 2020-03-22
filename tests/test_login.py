# from app import create_app
import unittest
import pytest

from tests.base import BaseTestCase

class FlaskTestCase(BaseTestCase):

    def test_index(self):
        # tester = app.test_client(self)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


    def test_login_page_loads(self):
        # tester = app.test_client(self)
        response = self.client.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()