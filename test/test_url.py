import unittest, tempfile
from .flask_learn.extensions import db
from flask_learn import create_app
import app
from flask_learn.resourses.route import *

class TestConfig():
    SQLALCHEMY_DATABASE_URI = 'postgresql://flask_learn:flask_learn@postgres:5432/flask_learn'

class TestURLs(unittest.TestCase):
    def setUp(self):
        app = create_app(TestConfig)
        self.client = app.client
        db.app = app
        db.create_all()
        

    def tearDown(self):
        db.session.remove()
        db.drop_all() 
        