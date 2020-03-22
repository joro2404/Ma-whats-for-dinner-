from flask_testing import TestCase
from werkzeug.security import generate_password_hash

from app import create_app
from app.user import User
from app.database import DB

class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app = create_app()
        return app

    def setUp(self):
        password = generate_password_hash("admin", method='sha256')
        user1 = User(None, "admin", password, "admin@admin.com", 76)
        user1.create()

    def tearDown(self):
        with DB() as db:
            db.execute(
                'DELETE FROM users WHERE username="admin"'
            )