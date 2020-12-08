import unittest

from training.app import app
from training.extensions import db


class setUpAndTearDown(unittest.TestCase):
    """
    Solution from: https://gist.github.com/twolfson/13f5f5784f67fd49b245

    The following code offers the possibility to have a common setUp and a tearDown, and also add
    a particular setUp and tearDown for each class.
    """

    @classmethod
    def setUpClass(cls):
        """On inherited classes, run our `setUp` method"""

        # Inspired via http://stackoverflow.com/questions/1323455/python-unit-test-with-base-and-sub-class/
        # 17696807#17696807

        if cls is not setUpAndTearDown and cls.setUp is not setUpAndTearDown.setUp:
            orig_setUp = cls.setUp

            def setUpOverride(self, *args, **kwargs):
                setUpAndTearDown.setUp(self)
                return orig_setUp(self, *args, **kwargs)
            cls.setUp = setUpOverride

    def setUp(self):
        """Do some custom setup for all tests here"""
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            db.session.commit()

        # Disable sending emails during unit testing
        self.assertEqual(app.debug, True)

    # executed after each test
    def tearDown(self):
        with app.app_context():
            db.drop_all()
            db.session.commit()
