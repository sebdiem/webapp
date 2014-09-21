#!flask/bin/python
import webapp
import unittest
import json

class WebappTestCase(unittest.TestCase):
    def setUp(self):
        webapp.app.config['TESTING'] = True
        self.app = webapp.app.test_client()

    def tearDown(self):
        pass

    def test_columns(self):
        rv = json.loads(self.app.get('/dataiku/columns').data)
        assert 'education' in rv['columns']
        assert 'age' in rv['columns']
        assert 'industry code' in rv['columns']

def runtests():
    unittest.main()

if __name__ == '__main__':
    runtests()

