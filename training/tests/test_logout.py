import unittest

from training.app_init import app, db
from training.models.users import User
from training.utils.test_funcions import create_one_user, login_one_user, logout


class BasicTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config.from_object('training.config.TestConfig')
        app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
        self.app = app.test_client()
        db.create_all()
        db.session.commit()

        # Disable sending emails during unit testing
        self.assertEqual(app.debug, True)

    # executed after each test
    def tearDown(self):
        db.drop_all()
        db.session.commit()

    # Tests inside
    def test_login_then_logout(self):
        with app.test_client() as client:
            username, password = create_one_user(client)
            login_one_user(client, username, password)

            self.assertEqual(200, client.get('/logout').status_code)

    def test_logout_without_login(self):
        with app.test_client() as client:
            # Decorator login_required catch the function and return 'no_login.html', 411
            self.assertEqual(411, client.get('/logout').status_code)

    def test_login_then_logout_two_times(self):
        with app.test_client() as client:
            username, password = create_one_user(client)
            login_one_user(client, username, password)

            # First logout should work as normal
            self.assertEqual(200, client.get('/logout').status_code)

            # Decorator login_required catch the function and return 'no_login.html', 411
            self.assertEqual(411, client.get('/logout').status_code)

    def test_login_3_users_logout_2(self):
        with app.test_client() as client:
            username1, password1 = create_one_user(client, username="Example1", email="sample1@g.com")
            username2, password2 = create_one_user(client, username="Example2", email="sample2@g.com")
            username3, password3 = create_one_user(client, username="Example3", email="sample3@g.com")
            login_one_user(client, username1, password1)
            login_one_user(client, username2, password2)
            login_one_user(client, username3, password3)

            # First logout should work as normal
            self.assertEqual(200, client.get('/logout').status_code)

            # Decorator login_required catch the function and return 'no_login.html', 411
            self.assertEqual(411, client.get('/logout').status_code)


if __name__ == "__main__":
    unittest.main()
