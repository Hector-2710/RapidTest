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

    def test_generate_id(self):
        result = Data.generate_id()
        self.assertIsInstance(result, str, "The result should be a string.")
        self.assertGreater(len(result), 1, "The result should be a valid UUID string.")

    def test_generate_email(self):
        result = Data.generate_email()
        self.assertIsInstance(result, str, "The result should be a string.")
        self.assertIn("@", result, "The result should contain '@'.")

    def test_generate_password(self):
        result = Data.generate_password()
        self.assertIsInstance(result, str, "The result should be a string.")
        self.assertGreater(len(result), 1, "The result should not be empty.")

    def test_generate_phone(self):
        result = Data.generate_phone()
        self.assertIsInstance(result, str, "The result should be a string.")
        self.assertGreater(len(result), 1, "The result should not be empty.")

    def test_generate_address(self):
        result = Data.generate_address()
        self.assertIsInstance(result, str, "The result should be a string.")
        self.assertGreater(len(result), 1, "The result should not be empty.")

    def test_generate_city(self):
        result = Data.generate_city()
        self.assertIsInstance(result, str, "The result should be a string.")
        self.assertGreater(len(result), 1, "The result should not be empty.")

    def test_generate_state(self):
        result = Data.generate_state()
        self.assertIsInstance(result, str, "The result should be a string.")

    def test_generate_zipcode(self):
        result = Data.generate_zipcode()
        self.assertIsInstance(result, str, "The result should be a string.")
        self.assertGreater(len(result), 1, "The result should not be empty.")

    def test_generate_country(self):
        result = Data.generate_country()
        self.assertIsInstance(result, str, "The result should be a string.")
        self.assertGreater(len(result), 1, "The result should not be empty.")

    def test_generate_job(self):
        result = Data.generate_job()
        self.assertIsInstance(result, str, "The result should be a string.")
        self.assertGreater(len(result), 1, "The result should not be empty.")

    def test_generate_text(self):
        result = Data.generate_text()
        self.assertIsInstance(result, str, "The result should be a string.")
        self.assertGreater(len(result), 1, "The result should not be empty.")

    def test_generate_paragraph(self):
        result = Data.generate_paragraph()
        self.assertIsInstance(result, str, "The result should be a string.")
        self.assertGreater(len(result), 1, "The result should not be empty.")

    def test_generate_date(self):
        result = Data.generate_date()
        self.assertIsInstance(result, str, "The result should be a string.")
        self.assertGreater(len(result), 1, "The result should not be empty.")

    def test_generate_datetime(self):
        result = Data.generate_datetime()
        self.assertIsInstance(result, str, "The result should be a string.")
        self.assertGreater(len(result), 1, "The result should not be empty.")

    def test_generate_time(self):
        result = Data.generate_time()
        self.assertIsInstance(result, str, "The result should be a string.")
        self.assertGreater(len(result), 1, "The result should not be empty.")

    def test_generate_url(self):
        result = Data.generate_url()
        self.assertIsInstance(result, str, "The result should be a string.")
        self.assertIn("http", result, "The result should start with 'http'.")

    def test_generate_domain(self):
        result = Data.generate_domain()
        self.assertIsInstance(result, str, "The result should be a string.")
        self.assertGreater(len(result), 1, "The result should not be empty.")

    def test_generate_ipv4(self):
        result = Data.generate_ipv4()
        self.assertIsInstance(result, str, "The result should be a string.")
        parts = result.split(".")
        self.assertEqual(len(parts), 4, "IPv4 should have 4 parts.")

    def test_generate_company(self):
        result = Data.generate_company()
        self.assertIsInstance(result, str, "The result should be a string.")
        self.assertGreater(len(result), 1, "The result should not be empty.")

    def test_generate_company_email(self):
        result = Data.generate_company_email()
        self.assertIsInstance(result, str, "The result should be a string.")
        self.assertIn("@", result, "The result should contain '@'.")

    def test_generate_product_name(self):
        result = Data.generate_product_name()
        self.assertIsInstance(result, str, "The result should be a string.")
        self.assertGreater(len(result), 1, "The result should not be empty.")

    def test_generate_price_default(self):
        result = Data.generate_price()
        self.assertIsInstance(result, str, "The result should be a string.")
        self.assertIn(".", result, "The result should contain a decimal point.")
        price_value = float(result)
        self.assertGreaterEqual(price_value, 1.0)
        self.assertLessEqual(price_value, 1000.0)

    def test_generate_price_custom_range(self):
        result = Data.generate_price(min_price=10.0, max_price=50.0)
        self.assertIsInstance(result, str, "The result should be a string.")
        price_value = float(result)
        self.assertGreaterEqual(price_value, 10.0)
        self.assertLessEqual(price_value, 50.0)

    def test_generate_users_default(self):
        result = Data.generate_users()
        self.assertIsInstance(result, list, "The result should be a list.")
        self.assertEqual(len(result), 1, "Default count should be 1.")
        self.assertIsInstance(result[0], dict, "Each item should be a dictionary.")

    def test_generate_users_custom_count(self):
        result = Data.generate_users(count=5)
        self.assertIsInstance(result, list, "The result should be a list.")
        self.assertEqual(len(result), 5, "Should generate 5 users.")

    def test_generate_users_with_fields(self):
        result = Data.generate_users(count=2, fields=["name", "email"])
        self.assertIsInstance(result, list, "The result should be a list.")
        self.assertEqual(len(result), 2, "Should generate 2 users.")
        self.assertIn("name", result[0], "User should have 'name' field.")
        self.assertIn("email", result[0], "User should have 'email' field.")
        self.assertNotIn("id", result[0], "User should not have 'id' field.")

    def test_generate_companies_default(self):
        result = Data.generate_companies()
        self.assertIsInstance(result, list, "The result should be a list.")
        self.assertEqual(len(result), 1, "Default count should be 1.")
        self.assertIsInstance(result[0], dict, "Each item should be a dictionary.")
        self.assertIn("name", result[0])
        self.assertIn("email", result[0])
        self.assertIn("address", result[0])
        self.assertIn("city", result[0])
        self.assertIn("country", result[0])

    def test_generate_companies_custom_count(self):
        result = Data.generate_companies(count=3)
        self.assertIsInstance(result, list, "The result should be a list.")
        self.assertEqual(len(result), 3, "Should generate 3 companies.")

    def test_generate_products_default(self):
        result = Data.generate_products()
        self.assertIsInstance(result, list, "The result should be a list.")
        self.assertEqual(len(result), 1, "Default count should be 1.")
        self.assertIn("name", result[0])
        self.assertIn("price", result[0])

    def test_generate_products_without_price(self):
        result = Data.generate_products(include_price=False)
        self.assertIsInstance(result, list, "The result should be a list.")
        self.assertIn("name", result[0])
        self.assertNotIn("price", result[0])

    def test_generate_products_custom_count(self):
        result = Data.generate_products(count=4)
        self.assertIsInstance(result, list, "The result should be a list.")
        self.assertEqual(len(result), 4, "Should generate 4 products.")


if __name__ == "__main__":
    unittest.main()
