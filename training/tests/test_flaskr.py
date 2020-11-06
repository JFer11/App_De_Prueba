import unittest
from flask import Flask


class TestSuite(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.from_pyfile(config_filename)

    def test_mi_test(self):
        # Código que se quiere probar
        pass

    def tearDown(self):
        # Código que se ejecuta después de cada test
        pass
