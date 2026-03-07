import unittest
from rapidtest.RapidData import data 

class TestData(unittest.TestCase):
    def test_create_auth_user(self):
        result = data.generate_auth_user()
        
        self.assertIsInstance(result, dict, "The result should be a dictionary.")
        
        self.assertIn('username', result, "The result should contain the key 'username'.")
        self.assertIn('password', result, "The result should contain the key 'password'.")
        
        self.assertTrue(result['username'], "The 'username' value should not be empty.")
        self.assertTrue(result['password'], "The 'password' value should not be empty.")

if __name__ == '__main__':
    unittest.main()