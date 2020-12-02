from itsdangerous import URLSafeTimedSerializer
import os

from training.extensions import bcrypt

serializer = URLSafeTimedSerializer(os.environ.get('SECRET_KEY'))


def crypt_password(raw):
    """returns the hash (hashed password) from an raw string"""

    return bcrypt.generate_password_hash(raw).decode('utf-8')
