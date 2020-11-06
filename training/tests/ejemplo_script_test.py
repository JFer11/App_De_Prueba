from flask import Flask
from flask_testing import TestCase


class MyTest(TestCase):

    def create_app(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost/baseparatesting'
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy.ext.declarative import declarative_base
        self.Base = declarative_base()
        self.engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/baseparatesting')
        Session = sessionmaker(self.engine)
        self.session = Session()

    def setUp(self):
        self.Base.metadata.create_all(self.engine)
        #db.create_all()

    def tearDown(self):
        pass
        #db.session.remove()
        #db.drop_all()

    def test_hola(self):
        a = True
        assert a is True
