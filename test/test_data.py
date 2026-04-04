import unittest

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from rapidtest.data import Data


class TestData(unittest.TestCase):
    def test_create_auth_user(self):
        result = Data.generate_auth_user()

        self.assertIsInstance(result, dict, "The result should be a dictionary.")

        self.assertIn(
            "username", result, "The result should contain the key 'username'."
        )
        self.assertIn(
            "password", result, "The result should contain the key 'password'."
        )

        self.assertTrue(result["username"], "The 'username' value should not be empty.")
        self.assertTrue(result["password"], "The 'password' value should not be empty.")

    def test_create_user(self):
        result = Data.generate_user(
            fields=["id", "name", "username", "password", "email", "age", "address"]
        )

        self.assertIsInstance(result, dict, "The result should be a dictionary.")

        expected_keys = [
            "id",
            "name",
            "username",
            "password",
            "email",
            "age",
            "address",
        ]
        for key in expected_keys:
            self.assertIn(key, result, f"The result should contain the key '{key}'.")
            self.assertTrue(result[key], f"The '{key}' value should not be empty.")

    def test_create_user_all_fields(self):
        result = Data.generate_user()
        self.assertIsInstance(result, dict, "The result should be a dictionary.")
        self.assertGreater(
            len(result), 0, "The result should contain fields by default."
        )

    def test_generate_name(self):
        result = Data.generate_name()
        self.assertIsInstance(result, str, "The result should be a string.")
        self.assertGreater(
            len(result), 1, "The result should be a string of length greater than 1."
        )


if __name__ == "__main__":
    unittest.main()
