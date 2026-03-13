import unittest

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from rapidtest.data import data 

class TestData(unittest.TestCase):
    def test_create_auth_user(self):
        result = data.generate_auth_user()
        
        self.assertIsInstance(result, dict, "The result should be a dictionary.")
        
        self.assertIn('username', result, "The result should contain the key 'username'.")
        self.assertIn('password', result, "The result should contain the key 'password'.")
        
        self.assertTrue(result['username'], "The 'username' value should not be empty.")
        self.assertTrue(result['password'], "The 'password' value should not be empty.")

    def test_create_user(self):
        result = data.generate_user(
            user_id=True, 
            name=True, 
            username=True, 
            password=True, 
            email=True, 
            age=True, 
            address=True
        )
        
        self.assertIsInstance(result, dict, "The result should be a dictionary.")
        
        expected_keys = ['id', 'name', 'username', 'password', 'email', 'age', 'address']
        for key in expected_keys:
            self.assertIn(key, result, f"The result should contain the key '{key}'.")
            self.assertTrue(result[key], f"The '{key}' value should not be empty.")

    def test_create_user_with_no_fields(self):
        result = data.generate_user()
        self.assertIsInstance(result, dict, "The result should be a dictionary.")
        self.assertEqual(len(result), 0, "The result should be an empty dictionary when no fields are requested.")

if __name__ == '__main__':
    unittest.main()