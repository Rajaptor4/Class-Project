import unittest
from app import app, db, BusData, UserData

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.ctx = app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()
        
    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_analytics_route(self):
        response = self.app.get('/analytics')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'total_buses', response.data)
        self.assertIn(b'total_users', response.data)

    def test_fetch_users_and_store(self):
        response = self.app.get('/fetch_users_and_store')
        self.assertEqual(response.status_code, 200)

        user_count_after = UserData.query.count()
        self.assertTrue(user_count_after > 0)

if __name__ == "__main__":
    unittest.main()

