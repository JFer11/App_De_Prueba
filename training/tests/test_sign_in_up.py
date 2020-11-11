import unittest

from training.app_init import app, db
from training.models.users import User


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

    # Create users Tests
    def test_sing_up_one_user(self):
        with app.test_client() as client:
            # We create a User
            self.assertEqual(client.post('/index', data=dict(username='Fernando Gago', email='Fernando@g.com', password='Fernando', confirm='Fernando', accept_tos=True), follow_redirects=True).status_code, 201)

            # We check if user 'Fernando Gago' was saved in the database
            self.assertNotEqual(None, User.query.filter_by(id="Fernando Gago").first())

    def test_sing_up_one_user_not_validate_form_bad_password(self):
        with app.test_client() as client:
            # We create a User, but password and confirmation does not match
            self.assertEqual(client.post('/index', data=dict(username='Fernando Gago', email='Fernando@g.com', passwords='password', confirm='another password', accept_tos=True), follow_redirects=True).status_code, 400)

    def test_sing_up_one_user_not_validate_form_short_username(self):
        with app.test_client() as client:
            # We create a User, but password and confirmation does not match
            self.assertEqual(client.post('/index', data=dict(username='F', email='Fernando@g.com', passwords='password', confirm='password', accept_tos=True), follow_redirects=True).status_code, 400)

    def test_sing_up_some_users_check_in_database(self):
        with app.test_client() as client:
            # We create four users
            self.assertEqual(client.post('/index', data=dict(username='Fernando1', email='Fernando1@g.com', password='Fernando', confirm='Fernando', accept_tos=True), follow_redirects=True).status_code, 201)
            self.assertEqual(client.post('/index', data=dict(username='Fernando2', email='Fernando2@g.com', password='Fernando', confirm='Fernando', accept_tos=True), follow_redirects=True).status_code, 201)
            self.assertEqual(client.post('/index', data=dict(username='Fernando3', email='Fernando3@g.com', password='Fernando', confirm='Fernando', accept_tos=True), follow_redirects=True).status_code, 201)
            self.assertEqual(client.post('/index', data=dict(username='Fernando4', email='Fernando4@g.com', password='Fernando', confirm='Fernando', accept_tos=True), follow_redirects=True).status_code, 201)

            # We checked if all users were created and saved in the database
            for i in range(1, 5):
                username = "Fernando" + str(i)
                self.assertNotEqual(None, User.query.filter_by(id=username).first())

    def test_sing_up_some_users_and_bad_credentials(self):
        print("-------------------------------")
        print("ESTE TEST HAY QUE DESAROLLARLO")
        print("-------------------------------")
        assert True
        # ERROR DESCUBIERTO, No se verifica que el mail no exista en la abse al momento de hacer sign up
        with app.test_client() as client:
            # We create two users, with same mail
            #self.assertEqual(client.post('/index', data=dict(username='Fernando1', email='Fernando1@g.com', password='Fernando', confirm='Fernando', accept_tos=True), follow_redirects=True).status_code, 201)
            #self.assertEqual(client.post('/index', data=dict(username='Fernando2', email='Fernando1@g.com', password='Fernando', confirm='Fernando', accept_tos=True), follow_redirects=True).status_code, 201)
            pass

    # Login Tests
    def test_sign_in_one_user_check_session(self):
        with app.test_client() as client:
            # We create a User
            self.assertEqual(client.post('/index', data=dict(username='Fernando', email='Fernando@g.com', password='Fernando', confirm='Fernando', accept_tos=True), follow_redirects=True).status_code, 201)

            # We have to validate the mail
            self.assertEqual(200, client.get('/mail/validation/Fernando').status_code)

            # We sign in with the recent user
            self.assertEqual(200, client.post('/login', data=dict(username='Fernando', password='Fernando'), follow_redirects=True).status_code)

            # We check if user's session was caught
            with client.session_transaction() as sess:
                self.assertEqual('Fernando', sess.get('username', None))

    def test_sign_in_bad_password(self):
        with app.test_client() as client:
            # We create a User
            self.assertEqual(client.post('/index', data=dict(username='Fernando', email='Fernando@g.com', password='Fernando', confirm='Fernando', accept_tos=True), follow_redirects=True).status_code, 201)

            # We have to validate the mail
            self.assertEqual(200, client.get('/mail/validation/Fernando').status_code)

            # We sign in with the recent user
            self.assertEqual(452, client.post('/login', data=dict(username='Fernando', password='wrong password'), follow_redirects=True).status_code)

            # We check if user's session was caught, result should be None cause it was not supposed to be in
            with client.session_transaction() as sess:
                self.assertEqual(None, sess.get('username', None))

    def test_sign_in_short_username(self):
        with app.test_client() as client:
            # We create a User
            self.assertEqual(client.post('/index', data=dict(username='Fernando', email='Fernando@g.com', password='Fernando', confirm='Fernando', accept_tos=True), follow_redirects=True).status_code, 201)

            # We have to validate the mail
            self.assertEqual(200, client.get('/mail/validation/Fernando').status_code)

            # We sign in with the recent user
            self.assertEqual(800, client.post('/login', data=dict(username='F', password='Fernando'), follow_redirects=True).status_code)
            # 800 means it was a successful GET, or an invalid POST FORM

            # We check if user's session was caught, result should be None cause it was not supposed to be in
            with client.session_transaction() as sess:
                self.assertEqual(None, sess.get('username', None))

    def test_sign_in_bad_username(self):
        with app.test_client() as client:
            # We create a User
            self.assertEqual(client.post('/index', data=dict(username='Fernando', email='Fernando@g.com', password='Fernando', confirm='Fernando', accept_tos=True), follow_redirects=True).status_code, 201)

            # We have to validate the mail
            self.assertEqual(200, client.get('/mail/validation/Fernando').status_code)

            # We sign in with the recent user
            self.assertEqual(450, client.post('/login', data=dict(username='wrong username', password='wrong password'), follow_redirects=True).status_code)

            # We check if user's session was caught, result should be None cause it was not supposed to be in
            with client.session_transaction() as sess:
                self.assertEqual(None, sess.get('username', None))

    def test_sign_in_several_users(self):
        with app.test_client() as client:
            # We create four users
            self.assertEqual(client.post('/index', data=dict(username='Fernando', email='Fernando@g.com', password='Fernando', confirm='Fernando', accept_tos=True), follow_redirects=True).status_code, 201)
            self.assertEqual(client.post('/index', data=dict(username='Fernando2', email='Fernando2@g.com', password='Fernando', confirm='Fernando', accept_tos=True), follow_redirects=True).status_code, 201)
            self.assertEqual(client.post('/index', data=dict(username='Fernando3', email='Fernando3@g.com', password='Fernando', confirm='Fernando', accept_tos=True), follow_redirects=True).status_code, 201)
            self.assertEqual(client.post('/index', data=dict(username='Fernando4', email='Fernando4@g.com', password='Fernando', confirm='Fernando', accept_tos=True), follow_redirects=True).status_code, 201)

            # We have to validate the all emails
            self.assertEqual(200, client.get('/mail/validation/Fernando').status_code)
            self.assertEqual(200, client.get('/mail/validation/Fernando2').status_code)
            self.assertEqual(200, client.get('/mail/validation/Fernando3').status_code)
            self.assertEqual(200, client.get('/mail/validation/Fernando4').status_code)

            # We log in all users
            self.assertEqual(200, client.post('/login', data=dict(username='Fernando', password='Fernando'), follow_redirects=True).status_code)
            self.assertEqual(200, client.post('/login', data=dict(username='Fernando2', password='Fernando'), follow_redirects=True).status_code)
            self.assertEqual(200, client.post('/login', data=dict(username='Fernando3', password='Fernando'), follow_redirects=True).status_code)
            self.assertEqual(200, client.post('/login', data=dict(username='Fernando4', password='Fernando'), follow_redirects=True).status_code)

            # We check last session, should be last user who logged in
            with client.session_transaction() as sess:
                self.assertEqual("Fernando4", sess.get("username"))

    def test_sing_in_two_times_same_user(self):
        with app.test_client() as client:
            # We create one user
            self.assertEqual(client.post('/index', data=dict(username='Fernando', email='Fernando@g.com', password='Fernando', confirm='Fernando', accept_tos=True), follow_redirects=True).status_code, 201)

            # We have validate the email
            self.assertEqual(200, client.get('/mail/validation/Fernando').status_code)

            # We log in two times the user
            self.assertEqual(200, client.post('/login', data=dict(username='Fernando', password='Fernando'), follow_redirects=True).status_code)
            self.assertEqual(200, client.post('/login', data=dict(username='Fernando', password='Fernando'), follow_redirects=True).status_code)

            # We check last session, should be the user, our app does not care about double log in yet
            with client.session_transaction() as sess:
                self.assertEqual("Fernando", sess.get("username"))

    # Mail validation Tests
    def test_sign_up_and_mail_validation_several_cases(self):
        with app.test_client() as client:
            # We create two User
            self.assertEqual(client.post('/index', data=dict(username='Fernando', email='Fernando@g.com', password='Fernando', confirm='Fernando', accept_tos=True), follow_redirects=True).status_code, 201)
            self.assertEqual(client.post('/index', data=dict(username='Fernando2', email='Fernando2@g.com', password='Fernando', confirm='Fernando', accept_tos=True), follow_redirects=True).status_code, 201)

            # We have to validate the mail well
            self.assertEqual(200, client.get('/mail/validation/Fernando').status_code)
            # We validate again the mail
            self.assertEqual(205, client.get('/mail/validation/Fernando').status_code)
            # We try to validate a mail from a wrong username
            self.assertEqual(450, client.get('/mail/validation/Fernandosdf').status_code)
            # We validate the other users's email
            self.assertEqual(200, client.get('/mail/validation/Fernando2').status_code)
            # We validate again same users's email
            self.assertEqual(205, client.get('/mail/validation/Fernando2').status_code)

            # We sign in both user
            self.assertEqual(200, client.post('/login', data=dict(username='Fernando', password='Fernando'), follow_redirects=True).status_code)
            self.assertEqual(200, client.post('/login', data=dict(username='Fernando2', password='Fernando'), follow_redirects=True).status_code)

            # We check if user's session was caught
            with client.session_transaction() as sess:
                self.assertEqual('Fernando2', sess.get('username', None))

    def test_sign_up_without_mail_validation(self):
        with app.test_client() as client:
            # We create a User
            self.assertEqual(client.post('/index', data=dict(username='Fernando', email='Fernando@g.com', password='Fernando', confirm='Fernando', accept_tos=True), follow_redirects=True).status_code, 201)

            # We sign in without mail validation
            self.assertEqual(451, client.post('/login', data=dict(username='Fernando', password='Fernando'), follow_redirects=True).status_code)

            # We check if user's session was caught, result should be None cause it was not supposed to be in
            with client.session_transaction() as sess:
                self.assertEqual(None, sess.get('username', None))


if __name__ == "__main__":
    unittest.main()
