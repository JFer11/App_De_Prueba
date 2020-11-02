import os


# default config
class BaseConfig(object):
    DEBUG = False
    # shortened for readability
    #SECRET_KEY = '\xbf\xb0\x11\xb1\xcd\xf9\xba\x8bp\x0c...'
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USE_SSL = False
    MAIL_USE_TLS = False
    MAIL_DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(BaseConfig):
    DEBUG = True    #Algunos lo ponen Flase, ver diferencias
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL_FOR_TEST']


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False