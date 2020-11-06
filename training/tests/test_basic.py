import os
import unittest
from time import sleep

from training.app_init import app, db
from flask import request
from flask import session

#from training.controllers.all_controllers import sesion as session
from training.models.users import User
from training.utils.common_functions import crypt_password
from training.utils.test_funcions import create_one_user


class BasicTests(unittest.TestCase):
    # executed prior to each test

    def setUp(self):
        app.config.from_object('training.config.TestConfig')
        app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
        self.app = app.test_client()
        #db.drop_all()
        db.create_all()
        db.session.commit()

        # Disable sending emails during unit testing
        self.assertEqual(app.debug, True)

    # executed after each test
    def tearDown(self):
        db.drop_all()
        db.session.commit()



    # Tests
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Hacer la make response del coso

    def test_request_basic(self):
        with app.test_request_context('/?name=Peter'):
            assert request.path == '/'
            assert request.args['name'] == 'Peter'

    def test_request_basic_2(self):
        with app.test_request_context('/'):
            assert request.path == '/'

    def test_no_session(self):
        with app.test_request_context('/'):
            assert session.get('username') == None


    def test_session_cookies(self):
        password = crypt_password('Fernando')
        db.session.add(User(id="Fernando", username="Fernando", email="test@gmail.com", password=password, mail_validation=True))
        db.session.commit()

        with app.test_client() as client:
            #with app.test_request_context('/login', method='POST'):
            client.post('/login', data=dict(username="Fernando", password="Fernando"), follow_redirects=True)
            assert session.get('username') == 'Fernando'


    def test_register_one_user(self):
        with app.test_client() as client:
            password = crypt_password('Fernando')
            client.post('/index', data=dict(username="Fernando Gago", email="ElMejorEjemplo@g.com", password=password, confirm=password, accept_tos=True), follow_redirects=True)
            our_user = User.query.filter_by(id="Fernando Gago").first()
            assert our_user is not None


    def test_register_more_users(self):
        with app.test_client() as client:
            passwords = [crypt_password('Fernando'), crypt_password('Gonzalo'), crypt_password('Nicolas'), crypt_password('Pedro')]
            ids = []
            for i in range(0,4):
                client.post('/index', data=dict(username="Fernando Gago"+str(i), email="ElMejorEjemplo@g.com"+str(i), password=passwords[i],
                                                confirm=passwords[i], accept_tos=True), follow_redirects=True)
                ids.append("Fernando Gago"+str(i))

            for id_user in ids:
                our_user = User.query.filter_by(id=id_user).first()
                assert our_user is not None


    def test_login_required_no_sesion(self):
        with app.test_client() as client:
            response1 = self.app.get('/inside', follow_redirects=True)
            response2 = self.app.get('/logout', follow_redirects=True)
            response3 = self.app.get('/ver', follow_redirects=True)
            self.assertEqual(response1.status_code, 411)
            self.assertEqual(response2.status_code, 411)
            self.assertEqual(response3.status_code, 411)



    """
    def test_ejemplo_session(self):
        with app.test_request_context('/login', data=dict(username="FernandoSAS", password=password), follow_redirects=True):
            assert session.get('username') == None
    """





    def test_sesion_after_sing_up(self):
        #with app.app_context():
        with app.test_client() as client:
            client.post('/index', data=dict(username="FernandoSAS", email="ElMejorEjemplo@g.com", password='Fernando', confirm='Fernando', accept_tos=True), follow_redirects=False)
            # We update mail_validation
            our_user = User.query.filter_by(id="FernandoSAS").first()
            our_user.mail_validation = True
            db.session.commit()

            client.post('/login', data=dict(username="FernandoSAS", password='Fernando'), follow_redirects=False)

            with client.session_transaction() as sess:
                assert sess.get('username') == 'FernandoSAS'



    def test_login_required_with_sesion(self):
        with app.test_client() as client:
            client.post('/index', data=dict(username="Fernando", email="ElMejorEjemplo@g.com", password='Fernando', confirm='Fernando', accept_tos=True), follow_redirects=False)
            our_user = User.query.filter_by(id="Fernando").first()
            our_user.mail_validation = True
            db.session.commit()

            client.post('/login', data=dict(username="Fernando", password='Fernando'), follow_redirects=False)

            response1 = client.get('/inside', follow_redirects=True)
            response2 = client.get('/logout', follow_redirects=True)
            response3 = client.get('/ver', follow_redirects=True)

            assert response1.status_code == 200
            assert response2.status_code == 200
            assert response3.status_code == 411


    def test_login_required_with_sesion(self):
        with app.test_client() as client:
            client.post('/index', data=dict(username="Fernando", email="ElMejorEjemplo@g.com", password='Fernando', confirm='Fernando', accept_tos=True), follow_redirects=False)
            our_user = User.query.filter_by(id="Fernando").first()
            our_user.mail_validation = True
            db.session.commit()

            client.post('/login', data=dict(username="Fernando", password='Fernando'), follow_redirects=False)

            response1 = client.get('/inside', follow_redirects=True)
            response2 = client.get('/logout', follow_redirects=True)
            response3 = client.get('/ver', follow_redirects=True)

            assert response1.status_code == 200
            assert response2.status_code == 200
            assert response3.status_code == 411


    def test_no_login_error(self):
        with app.test_client() as client:
            response1 = client.get('/inside', follow_redirects=True)
            response2 = client.get('/logout', follow_redirects=True)
            response3 = client.get('/ver', follow_redirects=True)
            assert response1.status_code == 411
            assert response2.status_code == 411
            assert response3.status_code == 411



    def test_login_logout(self):
        with app.test_client() as client:
            username, password = create_one_user(client)
            data = dict(username=username, password=password)
            client.post('/login', data=data, follow_redirects=True)

            response1 = client.get('/logout')
            response2 = client.get('/logout')
            assert response1.status_code == 200
            assert response2.status_code == 411


    def test_before_request(self):
        with app.test_request_context('/g'):
            print("Hola")


    def test_return_test_g(self):
        with app.test_client() as client:
            a = client.get('/g')
            assert a.status_code == 411

            create_one_user(client)

            b = client.post('/login', data=dict(username='Fernando', password='Fernando'), follow_redirects=True)
            assert b.status_code == 200


if __name__ == "__main__":
    unittest.main()

