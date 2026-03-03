from faker import Faker
from typing import Dict, Annotated

fake = Faker()

class data:
    """
    Fake data provider for testing.
    
    This class uses the Faker library to generate realistic information 
    like names, emails, addresses, etc.
    """

    @staticmethod
    def generate_auth_user() -> Dict[str, str]:
        """Generates a dictionary with random username and password."""
        user = {"username": fake.user_name(), "password": fake.password()}
        return user   

    @staticmethod
    def generate_user(*, name: Annotated[bool, "Whether to generate a name"] = False, username: Annotated[bool, "Whether to generate a username"] = False, password: Annotated[bool, "Whether to generate a password"] = False, email: Annotated[bool, "Whether to generate an email"] = False, age: Annotated[bool, "Whether to generate an age"] = False, address: Annotated[bool, "Whether to generate an address"] = False) -> Dict[str, str]:
        """Generates a dictionary with random user information."""
        user = {}
        if name:
            user["name"] = fake.name()
        if username:
            user["username"] = fake.user_name()
        if password:
            user["password"] = fake.password()
        if email:
            user["email"] = fake.email()
        if age:
            user["age"] = str(fake.random_int(min=18, max=80))
        if address:
            user["address"] = fake.address()
        return user
       
    @staticmethod
    def generate_name() -> str:
        """Generates a random full name."""
        return fake.name()

    @staticmethod
    def generate_id() -> str:
        """Generates a unique UUID."""
        return fake.uuid4()

    @staticmethod
    def generate_email() -> str:
        """Generates a random email address."""
        return fake.email()

    @staticmethod
    def generate_password() -> str:
        """Generates a secure random password."""
        return fake.password()

    @staticmethod
    def generate_phone() -> str:
        """Generates a random phone number."""
        return fake.phone_number()

    @staticmethod
    def generate_address() -> str:
        """Generates a random postal address."""
        return fake.address()

    @staticmethod
    def generate_city() -> str:
        """Generates a random city name."""
        return fake.city()

    @staticmethod
    def generate_state() -> str:
        """Generates a random state/province name."""
        return fake.state()

    @staticmethod
    def generate_zipcode() -> str:
        """Generates a random postal code."""
        return fake.zipcode()

    @staticmethod
    def generate_country() -> str:
        """Generates a random country name."""
        return fake.country()

    @staticmethod
    def generate_job() -> str:
        """Generates a random job title."""
        return fake.job()

    @staticmethod
    def generate_text() -> str:
        """Generates random text (short paragraph)."""
        return fake.text()

    @staticmethod
    def generate_paragraph() -> str:
        """Generates a long random paragraph."""
        return fake.paragraph()

    @staticmethod
    def generate_date() -> str:
        """Generates a random date (ISO format)."""
        return str(fake.date())

    @staticmethod
    def generate_datetime() -> str:
        """Generates random date and time (ISO format)."""
        return str(fake.date_time())

    @staticmethod
    def generate_time() -> str:
        """Generates a random time."""
        return str(fake.time())
