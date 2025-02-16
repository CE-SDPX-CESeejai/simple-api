import unittest
from app import app 

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client() 
        self.app.testing = True

    def test_plus(self):
        test_cases = [
            (5, 6, 11),
            (5.7, 6.8, 12.5),
            (-5, -6, -11),
            (-5.7, -6.8, -12.5),
            (0, 0, 0),
            (0, 6, 6),
            (0, -6, -6),
            (5, -6, -1),
            (-5, 6, 1),
            (0, 6.8, 6.8),
            (0, -6.8, -6.8),
            (5, -6.8, -1.8),
            (-5.8, 6, 0.2),
        ]

        for a, b, expected in test_cases:
            response = self.app.get(f"/plus/{a}/{b}")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()["result"], expected)

    def test_invalid_input(self):
        response = self.app.get("/plus/abc/5") 
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

if __name__ == "__main__":
    unittest.main()
