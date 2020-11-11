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

    # Test imported function
    def test_create_one_user(self):
        with app.test_client() as client:
            username, password = create_one_user(client)

            # We check if user  was saved in the database
            self.assertNotEqual(None, User.query.filter_by(id=username).first())

    def test_login_one_user(self):
        with app.test_client() as client:
            username, password = create_one_user(client)
            login_one_user(client, username, password)

            # We check if user was logged in, we verify it, requesting the session
            with client.session_transaction() as sess:
                self.assertEqual(username, sess.get('username'))

    def test_logout(self):
        with app.test_client() as client:
            username, password = create_one_user(client)
            login_one_user(client, username, password)
            logout(client)

            # We check if user is still logged in, we verify it requesting the session
            with client.session_transaction() as sess:
                self.assertEqual(None, sess.get('username'))

    # Tests inside
    def test_login_then_inside(self):
        with app.test_client() as client:
            username, password = create_one_user(client)
            login_one_user(client, username, password)

            self.assertEqual(200, client.get('/inside').status_code)

    def test_inside_without_login(self):
        with app.test_client() as client:
            create_one_user(client)

            # The decorator login_required catch the function and return 'no_login.html', 411
            self.assertEqual(411, client.get('/inside', follow_redirects=True).status_code)

    def test_login_logout_inside(self):
        with app.test_client() as client:
            username, password = create_one_user(client)
            login_one_user(client, username, password)
            logout(client)

            # The decorator login_required catch the function and return 'no_login.html', 411
            self.assertEqual(411, client.get('/inside').status_code)

    def test_logout_without_login_then_inside(self):
        with app.test_client() as client:
            logout(client)

            # The decorator login_required catch the function and return 'no_login.html', 411
            self.assertEqual(411, client.get('/inside').status_code)


if __name__ == "__main__":
    unittest.main()
