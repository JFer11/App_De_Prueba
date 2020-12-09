import unittest
from unittest.mock import MagicMock, Mock
from unittest.mock import patch

from training.app import app
from training.extensions import mail, db
from training.models.users import User
from training.tests.super_class import SetUpAndTearDown
from training.utils.test_funcions import create_one_user_no_mail_validation


# from training.background_tasks.tasks import send_email_function


class BasicTestsRecoverEmail(SetUpAndTearDown):
    """
    We run this test with the following command:
    FLASK_ENV=testing python -m unittest training/tests/test_send_recover_email.py
    So then, FLASK_ENV=testing, and when we import our app,
    app.config will be configured as app.config.from_object('training.config.TestConfig')

    If you ran tests with de IDE, is probably that app.config was not configured properly, so perhaps
    some test will not assert

    Important: If you want to run tests from this module, with the IDE, is even more difficult, because
    not only you have to overwrite app.config.from_object('training.config.TestConfig'), but also
    you will have to import mail from training.extensions because app.mail will have the first configuration
    and will be set with Testing=False.
    To do so:
    The line below is ABSOLUTELY NECESSARY, if not, the
    mail will have the previous application that was configured with TESTING = False
    mail.init_app(app)
    """

    # executed prior to each test, setUp and tearDown, inherited from setUpAndTearDown class

    def setUp(self):
        """Do more custom setup just for this class here"""
        mail.suppress = True

    # Test imported function
    def test_create_one_user_no_mail_validation(self):
        with app.test_client() as client:
            username, password = create_one_user_no_mail_validation(client)

            self.assertNotEqual(None, User.query.filter_by(id=username).first())
            with client.session_transaction() as sess:
                self.assertEqual(None, sess.get('username'))

    # Tests email validation
    def test_function_mail_test(self):
        with app.test_client() as client:
            with mail.record_messages() as outbox:
                self.assertEqual(200, client.get('/mail').status_code)
                assert len(outbox) == 1
                assert outbox[0].subject == "Confirm Email"

    def test_send_email_sync(self):
        with app.test_client() as client:
            with mail.record_messages() as outbox:
                self.assertEqual(204, client.post('/send/email', data=dict(email_sender="sender@g.com",
                                                                           email_recipient="recipient@g.com",
                                                                           message_body="This is a message body!",
                                                                           send_now=True)).status_code)

                self.assertEqual(1, len(outbox))
                self.assertEqual("Recover your account", outbox[0].subject)

    @patch('training.app.app.task_queue.enqueue')
    def test_example_with_mock_send_email_async(self, mock):
        with app.test_client() as client:
            """
            Una nota para entender el uso de mock con patch con llamadas REST.
            Aca se importa training.app.app.task_queue.enqueue esta funcion, que va a ser sustituida.
            va a ser sustituida por la funcion 'mock' y debe pasarse como argumento al test.
            Dentro del test, nosotros podemos modificar su comportamiento, hacer que devuelva los valores que queremos
            (ejemplo: mock.return_value = 40), hacer que solo acepte determiandos paramoetros, etc.
            Para ver que cosas se pueden hacer, leer la documentacion de unittest.mock, o si no una funcion que nos
            puede ayudar es hacer dir(mock). dir(mock) nos dice todos los nombres que estan definidos en el modulo,
            ya sean variables, modulos, o funciones.

            En el ejemplo de acontinuacion, no vamos a modificar su comportamiento, solo vamos a checkear que 
            efectivamente se este llamando a la funcion, cuando hacemos una request HTTP POST. 
            En nuestro caso, haremos un POST a '/send/email', para enviar un mail asyncronicamente. Entonces, se deberá
            llamar a la funcion 'app.task_queue.enqueue', que se encuentra dentro de la view function '/send/email'.
            """

            mock.return_value = 40
            self.assertEqual(200, client.post('/send/email',
                                              data=dict(email_sender="sender@g.com", email_recipient="recipient@g.com",
                                                        message_body="ASYNC EMAIL, This is a message body!"),
                                              follow_redirects=True).status_code)

            mock.assert_called()

    @patch('training.app.app.task_queue.enqueue')
    def test_send_sync_and_async_emails(self, mock):
        with app.test_client() as client:
            self.assertEqual(204, client.post('/send/email', data=dict(email_sender="sender@g.com",
                                                                       email_recipient="recipient@g.com",
                                                                       message_body="SYNC MAIL This is a message body!",
                                                                       send_now=True)).status_code)
            self.assertEqual(200, client.post('/send/email', data=dict(email_sender="sender@g.com",
                                                                       email_recipient="recipient@g.com",
                                                                       message_body="ASYNC EMAIL This is a message body!",
                                                                       )).status_code)
            mock.assert_called()
