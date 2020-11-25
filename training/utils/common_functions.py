from flask import request, session
from itsdangerous import URLSafeTimedSerializer
import os

from training.extensions import bcrypt, db
from training.models.users import User

serializer = URLSafeTimedSerializer(os.environ.get('SECRET_KEY'))


def crypt_password(raw):
    """returns the hash (hashed password) from an raw string"""

    return bcrypt.generate_password_hash(raw).decode('utf-8')


def how_is_logged():
    """ returns username if any user is logged"""
    username = session.get('username')
    header = request.headers.get('auth_token')

    if username is not None:
        return username
    elif header is not None:
        username_token = serializer.loads(header, salt='login')

        user = db.session.query(User).filter_by(id=username_token).first()
        return user.username
    else:
        return None
