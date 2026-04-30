"""
Data: Fake data generation module.

Provides realistic fake data generation using the Faker library.
Useful for generating test data, mock users, and sample content.

Example:
    >>> from rapidtest import Data
    >>> user = Data.generate_user()
    >>> email = Data.generate_email()
    >>> Data.set_locale("es_ES")
    >>> name = Data.generate_name()  # Spanish name
"""

from faker import Faker
from typing import Annotated

fake = Faker()


class Data:
    """
    Data provider for testing.

    This class uses the Faker library to generate realistic information
    like names, emails, addresses, etc. All methods are static.

    Example:
        >>> Data.set_locale("es_ES")
        >>> Data.generate_name()
        'Carlos García'
        >>> Data.reset_locale()
    """

    @staticmethod
    def set_locale(locale: str) -> None:
        """
        Sets the locale for data generation.

        Args:
            locale: Locale code (e.g., 'es_ES', 'en_US', 'fr_FR', 'de_DE').
                    See Faker documentation for available locales.

        Example:
            >>> Data.set_locale("es_ES")  # Spanish data
            >>> Data.set_locale("en_US")  # US English data
            >>> Data.set_locale("ja_JP")  # Japanese data
        """
        global fake
        fake = Faker(locale)

    @staticmethod
    def reset_locale() -> None:
        """
        Resets Faker to default locale (en_US).

        Example:
            >>> Data.set_locale("es_ES")
            >>> Data.reset_locale()  # Back to English
        """
        global fake
        fake = Faker()

    @staticmethod
    def generate_auth_user() -> dict[str, str]:
        """
        Generates a dictionary with random username and password.

        Returns:
            A dictionary with 'username' and 'password' keys.

        Example:
            >>> Data.generate_auth_user()
            {'username': 'alice123', 'password': 'xJ9#kL2mNop'}
        """
        user = {"username": fake.user_name(), "password": fake.password()}
        return user

    @staticmethod
    def generate_user(
        fields: Annotated[
            list[str] | None, "List of fields to generate (None = all)"
        ] = None,
    ) -> dict[str, str]:
        """
        Generates a dictionary with random user information.

        Args:
            fields: List of fields to include. Available: 'id', 'name', 'username',
                    'password', 'email', 'age', 'address', 'phone', 'city', 'state',
                    'country', 'company'. If None, generates all fields.

        Returns:
            A dictionary with the requested user information fields.

        Example:
            >>> Data.generate_user()  # All fields
            {'id': '...', 'name': '...', 'email': '...', ...}
            >>> Data.generate_user(['name', 'email'])  # Only name and email
            {'name': 'Alice Garcia', 'email': 'alice@example.com'}
        """
        all_fields = {
            "id": lambda: fake.uuid4(),
            "name": lambda: fake.name(),
            "username": lambda: fake.user_name(),
            "password": lambda: fake.password(),
            "email": lambda: fake.email(),
            "age": lambda: str(fake.random_int(min=18, max=80)),
            "address": lambda: fake.address(),
            "phone": lambda: fake.phone_number(),
            "city": lambda: fake.city(),
            "state": lambda: fake.state(),
            "country": lambda: fake.country(),
            "company": lambda: fake.company(),
        }

        if fields is None:
            fields = list(all_fields.keys())

        user = {}
        for field in fields:
            if field in all_fields:
                user[field] = all_fields[field]()
        return user

    @staticmethod
    def generate_name() -> str:
        """
        Generates a random full name.

        Returns:
            A random full name as a string.

        Example:
            >>> Data.generate_name()
            'Carlos García'
        """
        return fake.name()

    @staticmethod
    def generate_id() -> str:
        """
        Generates a unique UUID.

        Returns:
            A unique UUID as a string.

        Example:
            >>> Data.generate_id()
            'a1b2c3d4-e5f6-7890-abcd-ef1234567890'
        """
        return fake.uuid4()

    @staticmethod
    def generate_email() -> str:
        """
        Generates a random email address.

        Returns:
            A random email address as a string.

        Example:
            >>> Data.generate_email()
            'alice.garcia@example.com'
        """
        return fake.email()

    @staticmethod
    def generate_password() -> str:
        """
        Generates a secure random password.

        Returns:
            A random password as a string.

        Example:
            >>> Data.generate_password()
            'xJ9#kL2mNop'
        """
        return fake.password()

    @staticmethod
    def generate_phone() -> str:
        """
        Generates a random phone number.

        Returns:
            A random phone number as a string.

        Example:
            >>> Data.generate_phone()
            '+1 (555) 123-4567'
        """
        return fake.phone_number()

    @staticmethod
    def generate_address() -> str:
        """
        Generates a random postal address.

        Returns:
            A random postal address as a string.

        Example:
            >>> Data.generate_address()
            '123 Main Street\\nApt 4B\\nNew York, NY 10001'
        """
        return fake.address()

    @staticmethod
    def generate_city() -> str:
        """
        Generates a random city name.

        Returns:
            A random city name as a string.

        Example:
            >>> Data.generate_city()
            'Barcelona'
        """
        return fake.city()

    @staticmethod
    def generate_state() -> str:
        """
        Generates a random state/province name.

        Returns:
            A random state/province name as a string.

        Example:
            >>> Data.generate_state()
            'California'
        """
        return fake.state()

    @staticmethod
    def generate_country() -> str:
        """
        Generates a random country name.

        Returns:
            A random country name as a string.

        Example:
            >>> Data.generate_country()
            'United States'
        """
        return fake.country()

    @staticmethod
    def generate_zipcode() -> str:
        """
        Generates a random postal code.

        Returns:
            A random postal code as a string.

        Example:
            >>> Data.generate_zipcode()
            '90210'
        """
        return fake.zipcode()

    @staticmethod
    def generate_job() -> str:
        """
        Generates a random job title.

        Returns:
            A random job title as a string.

        Example:
            >>> Data.generate_job()
            'Software Engineer'
        """
        return fake.job()

    @staticmethod
    def generate_text() -> str:
        """
        Generates random text (short paragraph).

        Returns:
            A random text as a string.

        Example:
            >>> Data.generate_text()
            'Sit vitae est natus et omnis architecto.'
        """
        return fake.text()

    @staticmethod
    def generate_paragraph() -> str:
        """
        Generates a long random paragraph.

        Returns:
            A random paragraph as a string.

        Example:
            >>> Data.generate_paragraph()
            'Lorem ipsum dolor sit amet...'
        """
        return fake.paragraph()

    @staticmethod
    def generate_date() -> str:
        """
        Generates a random date (ISO format).

        Returns:
            A random date as a string in ISO format.

        Example:
            >>> Data.generate_date()
            '2024-03-15'
        """
        return str(fake.date())

    @staticmethod
    def generate_datetime() -> str:
        """
        Generates random date and time (ISO format).

        Returns:
            A random date and time as a string in ISO format.

        Example:
            >>> Data.generate_datetime()
            '2024-03-15 14:30:00'
        """
        return str(fake.date_time())

    @staticmethod
    def generate_time() -> str:
        """
        Generates a random time.

        Returns:
            A random time as a string.

        Example:
            >>> Data.generate_time()
            '14:30:00'
        """
        return str(fake.time())

    @staticmethod
    def generate_url() -> str:
        """
        Generates a random URL.

        Returns:
            A random URL string.

        Example:
            >>> Data.generate_url()
            'https://www.example.com/page'
        """
        return fake.url()

    @staticmethod
    def generate_domain() -> str:
        """
        Generates a random domain name.

        Returns:
            A random domain string.

        Example:
            >>> Data.generate_domain()
            'example.com'
        """
        return fake.domain_name()

    @staticmethod
    def generate_ipv4() -> str:
        """
        Generates a random IPv4 address.

        Returns:
            A random IPv4 address string.

        Example:
            >>> Data.generate_ipv4()
            '192.168.1.1'
        """
        return fake.ipv4()

    @staticmethod
    def generate_company() -> str:
        """
        Generates a random company name.

        Returns:
            A random company name string.

        Example:
            >>> Data.generate_company()
            'Acme Corporation'
        """
        return fake.company()

    @staticmethod
    def generate_company_email() -> str:
        """
        Generates a random company email address.

        Returns:
            A random company email string.

        Example:
            >>> Data.generate_company_email()
            'info@acmecorp.com'
        """
        return fake.company_email()

    @staticmethod
    def generate_product_name() -> str:
        """
        Generates a random product name.

        Returns:
            A random product name string.

        Example:
            >>> Data.generate_product_name()
            'Ergonomic Granite Chair'
        """
        return fake.catch_phrase()

    @staticmethod
    def generate_price(min_price: float = 1.0, max_price: float = 1000.0) -> str:
        """
        Generates a random price.

        Args:
            min_price: Minimum price value (default: 1.0).
            max_price: Maximum price value (default: 1000.0).

        Returns:
            A random price as a formatted string with 2 decimals.

        Example:
            >>> Data.generate_price()
            '49.99'
            >>> Data.generate_price(min_price=10, max_price=100)
            '75.50'
        """
        import random

        price = random.uniform(min_price, max_price)
        return f"{price:.2f}"

    @staticmethod
    def generate_users(
        count: Annotated[int, "Number of users to generate"] = 1,
        fields: Annotated[list[str] | None, "Fields to include (None = all)"] = None,
    ) -> list[dict[str, str]]:
        """
        Generates a list of users.

        Args:
            count: Number of users to generate (default: 1).
            fields: List of fields to include. Available: 'id', 'name', 'username',
                    'password', 'email', 'age', 'address', 'phone', 'city', 'state',
                    'country', 'company'. If None, generates all fields.

        Returns:
            A list of user dictionaries.

        Example:
            >>> Data.generate_users(3)
            [{'id': '...', 'name': '...', ...}, ...]
            >>> Data.generate_users(2, ['name', 'email'])
            [{'name': 'Alice', 'email': 'alice@example.com'}, ...]
        """
        return [Data.generate_user(fields=fields) for _ in range(count)]

    @staticmethod
    def generate_companies(
        count: Annotated[int, "Number of companies to generate"] = 1,
    ) -> list[dict[str, str]]:
        """
        Generates a list of companies.

        Args:
            count: Number of companies to generate (default: 1).

        Returns:
            A list of company dictionaries with 'name', 'email', 'address', 'city'.

        Example:
            >>> Data.generate_companies(2)
            [{'name': 'Acme Corp', 'email': 'info@acme.com', ...}, ...]
        """
        return [
            {
                "name": fake.company(),
                "email": fake.company_email(),
                "address": fake.address(),
                "city": fake.city(),
                "country": fake.country(),
            }
            for _ in range(count)
        ]

    @staticmethod
    def generate_products(
        count: Annotated[int, "Number of products to generate"] = 1,
        include_price: Annotated[bool, "Include random price"] = True,
    ) -> list[dict[str, str]]:
        """
        Generates a list of products.

        Args:
            count: Number of products to generate (default: 1).
            include_price: Whether to include a random price (default: True).

        Returns:
            A list of product dictionaries with 'name', 'price' (optional).

        Example:
            >>> Data.generate_products(2)
            [{'name': 'Ergonomic Chair', 'price': '199.99'}, ...]
            >>> Data.generate_products(3, include_price=False)
            [{'name': 'Standing Desk'}, ...]
        """
        products = []
        for _ in range(count):
            product = {"name": fake.catch_phrase()}
            if include_price:
                product["price"] = Data.generate_price()
            products.append(product)
        return products