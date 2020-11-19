import unittest

from training.extensions import db
from training.app import app
from training.models.users import User
from training.utils.test_funcions import create_one_user, login_one_user, create_one_user_no_mail_validation


class BasicTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        # We run this test with the following command:
        # FLASK_ENV=testing python -m unittest training/tests/test_email_validation.py
        # So then, FLASK_ENV=testing, and when we import our app,
        # app.config will be configured as app.config.from_object('training.config.TestConfig')

        # If you ran tests with de IDE, is probably that app.config was not configured properly, so perhaps
        # some test will not assert

        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            db.session.commit()

        # Disable sending emails during unit testing
        self.assertEqual(app.debug, True)

    # executed after each test
    def tearDown(self):
        with app.app_context():
            db.drop_all()
            db.session.commit()

    # Test imported function
    def test_create_one_user_no_mail_validation(self):
        with app.test_client() as client:
            username, password = create_one_user(client)

            self.assertNotEqual(None, User.query.filter_by(id=username).first())
            with client.session_transaction() as sess:
                self.assertEqual(None, sess.get('username'))

    # Tests email validation
    def test_validate_one_user_then_login(self):
        with app.test_client() as client:
            # We create one user with no email validation
            username, password = create_one_user_no_mail_validation(client)

            # We validate his email
            self.assertEqual(200, client.get(f'/mail/validation/{username}').status_code)

            # We log in the user
            login_one_user(client, username, password)

            # We check if our user logged in correctly
            with client.session_transaction() as sess:
                self.assertEqual(username, sess.get('username'))

    def test_validate_mail_non_existent_user(self):
        with app.test_client() as client:
            username = "Non-existent user"
            self.assertEqual(450, client.get(f'/mail/validation/{username}').status_code)

    def test_validate_two_times_a_valid_username(self):
        with app.test_client() as client:
            # We create one user with no email validation
            username, password = create_one_user_no_mail_validation(client)

            # We validate his email for the first time
            self.assertEqual(200, client.get(f'/mail/validation/{username}').status_code)

            # We validate his email for the second time
            self.assertEqual(205, client.get(f'/mail/validation/{username}').status_code)

            # We log the user who just validated his email
            self.assertEqual(200, client.post('/login', data=dict(username=username, password=password), follow_redirects=True).status_code)

            # We check if out user logged in correctly
            with client.session_transaction() as sess:
                self.assertEqual(username, sess.get('username'))
