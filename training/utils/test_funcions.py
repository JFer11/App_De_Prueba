from training.models.users import User
from training.app import db


def create_one_user(client):
    data = dict(username="Fernando", email="ElMejorEjemplo@g.com", password='Fernando', confirm='Fernando',
                accept_tos=True)
    client.post('/index', data=data)
    our_user = User.query.filter_by(id='Fernando').first()
    our_user.mail_validation = True
    db.session.commit()

    return 'Fernando', 'Fernando'
