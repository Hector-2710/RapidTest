from faker import Faker
from typing import Dict

fake = Faker()

class Data:
    """
    Proveedor de datos ficticios para pruebas.
    
    Esta clase utiliza la librería Faker para generar información realista 
    como nombres, correos, direcciones, etc.
    """

    @staticmethod
    def generate_auth_user() -> Dict[str, str]:
        """Genera un diccionario con username y password aleatorios."""
        user = {"username": fake.user_name(), "password": fake.password()}
        return user   

    @staticmethod
    def generate_name() -> str:
        """Genera un nombre completo aleatorio."""
        return fake.name()

    @staticmethod
    def generate_id() -> str:
        """Genera un UUID único."""
        return fake.uuid4()

    @staticmethod
    def generate_email() -> str:
        """Genera un correo electrónico aleatorio."""
        return fake.email()

    @staticmethod
    def generate_password() -> str:
        """Genera una contraseña segura aleatoria."""
        return fake.password()

    @staticmethod
    def generate_phone() -> str:
        """Genera un número de teléfono aleatorio."""
        return fake.phone_number()

    @staticmethod
    def generate_address() -> str:
        """Genera una dirección postal aleatoria."""
        return fake.address()

    @staticmethod
    def generate_city() -> str:
        """Genera el nombre de una ciudad aleatoria."""
        return fake.city()

    @staticmethod
    def generate_state() -> str:
        """Genera el nombre de un estado/provincia aleatorio."""
        return fake.state()

    @staticmethod
    def generate_zipcode() -> str:
        """Genera un código postal aleatorio."""
        return fake.zipcode()

    @staticmethod
    def generate_country() -> str:
        """Genera el nombre de un país aleatorio."""
        return fake.country()

    @staticmethod
    def generate_company() -> str:
        """Genera el nombre de una empresa ficticia."""
        return fake.company()

    @staticmethod
    def generate_job() -> str:
        """Genera un título de trabajo aleatorio."""
        return fake.job()

    @staticmethod
    def generate_text() -> str:
        """Genera un texto aleatorio (párrafo corto)."""
        return fake.text()

    @staticmethod
    def generate_sentence() -> str:
        """Genera una oración aleatoria."""
        return fake.sentence()

    @staticmethod
    def generate_paragraph() -> str:
        """Genera un párrafo largo aleatorio."""
        return fake.paragraph()

    @staticmethod
    def generate_date() -> str:
        """Genera una fecha aleatoria (ISO)."""
        return str(fake.date())

    @staticmethod
    def generate_datetime() -> str:
        """Genera fecha y hora aleatoria (ISO)."""
        return str(fake.date_time())

    @staticmethod
    def generate_time() -> str:
        """Genera una hora aleatoria."""
        return str(fake.time())

    @staticmethod
    def generate_url() -> str:
        """Genera una URL aleatoria."""
        return fake.url()

