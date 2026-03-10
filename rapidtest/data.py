from faker import Faker
from typing import Dict, Annotated

fake = Faker()

class data:
    """
    Data provider for testing.
    
    This class uses the Faker library to generate realistic information 
    like names, emails, addresses, etc.
    """

    @staticmethod
    def generate_auth_user() -> Dict[str, str]:
        """Generates a dictionary with random username and password.

        Args:
            None
        Returns:
            A dictionary with 'username' and 'password' keys.
        """
        
        user = {"username": fake.user_name(), "password": fake.password()}
        return user   

    @staticmethod
    def generate_user(*, 
                     user_id: Annotated[bool, "Whether to generate an ID"] = False, 
                     name: Annotated[bool, "Whether to generate a name"] = False, 
                     username: Annotated[bool, "Whether to generate a username"] = False, 
                     password: Annotated[bool, "Whether to generate a password"] = False, 
                     email: Annotated[bool, "Whether to generate an email"] = False, 
                     age: Annotated[bool, "Whether to generate an age"] = False, 
                     address: Annotated[bool, "Whether to generate an address"] = False) -> Dict[str, str]:
        """Generates a dictionary with random user information.
        
        Args:
            user_id: Whether to include a unique ID in the user data
            name: Whether to include a full name in the user data
            username: Whether to include a username in the user data
            password: Whether to include a password in the user data
            email: Whether to include an email address in the user data
            age: Whether to include an age (18-80) in the user data
            address: Whether to include a postal address in the user data   

        Returns:
            A dictionary with the requested user information fields.
        """

        user = {}
        if user_id:
            user["id"] = fake.uuid4()
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
        """Generates a random full name.
        
        Args:   
            None
        Returns:
            A random full name as a string.
        """
        return fake.name()

    @staticmethod
    def generate_id() -> str:
        """Generates a unique UUID.
        Args:   
            None
        Returns:
            A unique UUID as a string.
        """
        return fake.uuid4()

    @staticmethod
    def generate_email() -> str:
        """Generates a random email address.
        Args:   
            None
        Returns:                
            A random email address as a string.
        """
        return fake.email()

    @staticmethod
    def generate_password() -> str:
        """Generates a secure random password.
        Args:   
            None
        Returns:                
            A random password as a string.
        """
        return fake.password()

    @staticmethod
    def generate_phone() -> str:
        """Generates a random phone number.
        Args:   
            None
        Returns:                
            A random phone number as a string.
        """
        return fake.phone_number()

    @staticmethod
    def generate_address() -> str:
        """Generates a random postal address.
        Args:   
            None
        Returns:                
            A random postal address as a string.
        """
        return fake.address()

    @staticmethod
    def generate_city() -> str:
        """Generates a random city name.
        Args:   
            None
        Returns:                
            A random city name as a string.
        """
        return fake.city()

    @staticmethod
    def generate_state() -> str:
        """Generates a random state/province name.
        Args:   
            None
        Returns:                
            A random state/province name as a string.
        """
        return fake.state()

    @staticmethod
    def generate_zipcode() -> str:
        """Generates a random postal code.
        Args:   
            None
        Returns:                
            A random postal code as a string.
        """
        return fake.zipcode()

    @staticmethod
    def generate_country() -> str:
        """Generates a random country name.
        Args:   
            None
        Returns:                
            A random country name as a string.
        """
        return fake.country()

    @staticmethod
    def generate_job() -> str:
        """Generates a random job title.
        Args:   
            None
        Returns:                
            A random job title as a string.
        """
        return fake.job()

    @staticmethod
    def generate_text() -> str:
        """Generates random text (short paragraph).
        Args:   
            None
        Returns:                
            A random text as a string.  
        """
        return fake.text()

    @staticmethod
    def generate_paragraph() -> str:
        """Generates a long random paragraph.
        Args:   
            None
        Returns:
            A random paragraph as a string.
        """
        return fake.paragraph()

    @staticmethod
    def generate_date() -> str:
        """Generates a random date (ISO format).
        Args:   
            None
        Returns:
            A random date as a string.
        """
        return str(fake.date())

    @staticmethod
    def generate_datetime() -> str:
        """Generates random date and time (ISO format).
        Args:   
            None
        Returns:
            A random date and time as a string.
        """
        return str(fake.date_time())

    @staticmethod
    def generate_time() -> str:
        """Generates a random time.
        Args:   
            None
        Returns:
            A random time as a string.
        """
        return str(fake.time())
