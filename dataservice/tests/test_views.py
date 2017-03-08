import unittest
from dataservice.app import app
from flask_webtest import TestApp as _TestApp


class TestViews(unittest.TestCase):
    def setUp(self):
        self.app = _TestApp(app)

    def test_one(self):
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 200)
