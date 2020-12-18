import os


# default config
class BaseConfig(object):
    DEBUG = False
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USE_SSL = False
    MAIL_USE_TLS = False
    MAIL_DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')


class TestConfig(BaseConfig):
    DEBUG = True    #Algunos lo ponen Flase, ver diferencias
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL_FOR_TEST']
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    MAIL_SUPPRESS_SEND = True


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
