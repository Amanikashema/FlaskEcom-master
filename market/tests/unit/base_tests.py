from unittest import TestCase
from market import db
from market import app


class BaseTest(TestCase):
    def setUp(self):
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        with app.app_context():
            db.create_all()
        self.app = app.test_client()
        self.app_context = app.app_context()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
