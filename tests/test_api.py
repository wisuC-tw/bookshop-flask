import unittest
import requests

class ApiTest(unittest.TestCase):
    API_URL = "http://127.0.0.1:5000"

    def test_index(self):
        r = requests.get(ApiTest.API_URL)
        self.assertEqual(200, r.status_code)
        self.assertIn("Index Page", r.text)

    def test_home(self):
        r = requests.get(ApiTest.API_URL + "/hello")
        self.assertEqual(200, r.status_code)
        self.assertIn("Hello, World", r.text)
