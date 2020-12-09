from training.extensions import bcrypt


def crypt_password(raw):
    """returns the hash (hashed password) from an raw string"""

    return bcrypt.generate_password_hash(raw).decode('utf-8')
