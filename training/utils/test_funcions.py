from training.models.users import User
from training.extensions import db


def create_one_user(client, username="Fernando", email="ElMejorEjemplo@g.com", password='Fernando', confirm='Fernando', accept_tos=True):
    data = dict(username=username, email=email, password=password, confirm=confirm,
                accept_tos=accept_tos)
    client.post('/register', data=data)
    our_user = User.query.filter_by(id=username).first()
    our_user.mail_validation = True
    db.session.commit()

    return username, password


def create_one_user_no_mail_validation(client, username="Fernando", email="ElMejorEjemplo@g.com", password='Fernando', confirm='Fernando', accept_tos=True):
    data = dict(username=username, email=email, password=password, confirm=confirm,
                accept_tos=accept_tos)
    client.post('/register', data=data)

    return username, password


def login_one_user(client, username, password):
    data = dict(username=username, password=password)
    client.post('/login', data=data, follow_redirects=True)


def logout(client):
    client.get('/logout')
