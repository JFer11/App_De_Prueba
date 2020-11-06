from flask_testing import TestCase

from training.app_init import app, db
from training.models.users import User


class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.add(User("admin", "ad@min.com", "admin"))
        db.session.commit()
        assert True

    def tearDown(self):
        db.session.remove()
        db.drop_all()
