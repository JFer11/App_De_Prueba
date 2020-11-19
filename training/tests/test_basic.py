import unittest

from training.app import app
from training.extensions import db
from flask import request
from flask import session

from training.models.users import User
from training.utils.common_functions import crypt_password
from training.utils.test_funcions import create_one_user, login_one_user


class BasicTests(unittest.TestCase):
    # executed prior to each test

    def setUp(self):
        # We run this test with the following command:
        # FLASK_ENV=testing python -m unittest training/tests/test_basic.py
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

    # Tests
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_request_basic(self):
        with app.test_request_context('/?name=Peter'):
            self.assertEqual('/', request.path)
            self.assertEqual('Peter', request.args['name'])

    def test_request_basic_two(self):
        with app.test_request_context('/'):
            self.assertEqual(request.path, '/')

    def test_no_session(self):
        with app.test_request_context('/'):
            self.assertIsNone(session.get('username'))

    def test_session_cookies(self):
        password = crypt_password('Fernando')
        with app.app_context():
            db.session.add(User(id="Fernando", username="Fernando", email="test@gmail.com",
                                password=password, mail_validation=True))
            db.session.commit()

        with app.test_client() as client:
            client.post('/login', data=dict(username="Fernando", password="Fernando"), follow_redirects=True)
            self.assertEqual('Fernando', session.get('username'))

    def test_login_required_no_session(self):
        with app.test_client() as client:
            response1 = client.get('/inside', follow_redirects=True)
            response2 = client.get('/logout', follow_redirects=True)
            response3 = client.get('/ver', follow_redirects=True)
            self.assertEqual(response1.status_code, 411)
            self.assertEqual(response2.status_code, 411)
            self.assertEqual(response3.status_code, 411)

    def test_session_after_sing_up(self):
        with app.test_client() as client:
            client.post('/register', data=dict(username="FernandoSAS", email="ElMejorEjemplo@g.com",
                                               password='Fernando',
                                               confirm='Fernando', accept_tos=True), follow_redirects=False)
            # We update mail_validation
            our_user = User.query.filter_by(id="FernandoSAS").first()
            our_user.mail_validation = True
            db.session.commit()

            client.post('/login', data=dict(username="FernandoSAS", password='Fernando'), follow_redirects=False)

            with client.session_transaction() as sess:
                self.assertEqual('FernandoSAS', sess.get('username'))

    def test_login_required_with_sesion(self):
        with app.test_client() as client:
            client.post('/register', data=dict(username="Fernando", email="ElMejorEjemplo@g.com", password='Fernando',
                                               confirm='Fernando', accept_tos=True), follow_redirects=False)
            our_user = User.query.filter_by(id="Fernando").first()
            our_user.mail_validation = True
            db.session.commit()

            client.post('/login', data=dict(username="Fernando", password='Fernando'), follow_redirects=False)

            response1 = client.get('/inside', follow_redirects=True)
            response2 = client.get('/logout', follow_redirects=True)
            response3 = client.get('/ver', follow_redirects=True)

            self.assertEqual(200, response1.status_code)
            self.assertEqual(200, response2.status_code)
            self.assertEqual(411, response3.status_code)

    def test_g_after_login(self):
        with app.test_client() as client:
            username, password = create_one_user(client)
            login_one_user(client, username, password)
            self.assertEqual(200, client.get('/g').status_code)

    def test_g_before_login(self):
        with app.test_client() as client:
            self.assertEqual(411, client.get('/g').status_code)

    def test_return_test_g(self):
        with app.test_client() as client:

            a = client.get('/g')
            self.assertEqual(411, a.status_code)

            create_one_user(client)

            b = client.post('/login', data=dict(username='Fernando', password='Fernando'), follow_redirects=True)
            self.assertEqual(200, b.status_code)
