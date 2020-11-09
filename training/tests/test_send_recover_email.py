import unittest
from time import sleep

from training.app_init import app, db
from training.app import mail
from training.models.users import User
from training.utils.test_funcions import create_one_user, login_one_user, logout, create_one_user_no_mail_validation


class BasicTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config.from_object('training.config.TestConfig')
        app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
        self.app = app.test_client()
        db.create_all()
        db.session.commit()
        #print(app.config)
        print(mail.app.config)
        print(mail)

        # Disable sending emails during unit testing
        self.assertEqual(app.debug, True)

    # executed after each test
    def tearDown(self):
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
    def test_prueba_mail(self):
        with app.test_client() as client:
            with mail.record_messages() as outbox:
                self.assertEqual(200, client.get('/mail').status_code)
                assert len(outbox) == 1
                assert outbox[0].subject == "Confirm Email"

    def test_send_email_sync(self):
        with app.test_client() as client:
            with mail.record_messages() as outbox:
                self.assertEqual(200, client.post('/send/email', data=dict(email_sender="sender@g.com", email_recipient="recipient@g.com", message_body="JHGF This is a message body!", send_now=True)).status_code)

                self.assertEqual(1, len(outbox))
                self.assertEqual("Recover your account", outbox[0].subject)

    """
    def test_send_email_async(self):
        with app.test_client() as client:
            with mail.record_messages() as outbox:
                self.assertEqual(200, client.post('/send/email', data=dict(email_sender="sender@g.com", email_recipient="recipient@g.com", message_body="ASYNC EMAIL, This is a message body!"), follow_redirects=True).status_code)

                sleep(3)
                self.assertEqual(1, len(outbox))
                self.assertEqual("Recover your account", outbox[0].subject)
    """


if __name__ == "__main__":
    unittest.main()
