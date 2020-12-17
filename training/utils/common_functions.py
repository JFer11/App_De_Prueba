from training.extensions import bcrypt
from training.models.users import User


def crypt_password(raw):
    """returns the hash (hashed password) from an raw string"""

    return bcrypt.generate_password_hash(raw).decode('utf-8')


def test_unique_fields(username, email):
    if User.query.filter_by(id=username).first() or User.query.filter_by(email=email).first() is not None:
        return False
    else:
        return True
