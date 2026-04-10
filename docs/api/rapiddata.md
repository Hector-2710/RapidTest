# Data Generation API

Random data generator for testing using the Faker library.

```python
from rapidtest import Data
```

## Data Class

Static class providing fake data generation methods for testing purposes.

### Personal Information

#### generate_name

```python
Data.generate_name() -> str
```

Generates a random full name.

**Example:**
```python
name = Data.generate_name()
print(name)  # "John Smith"
```

#### generate_email

```python
Data.generate_email() -> str
```

Generates a random email address.

**Example:**
```python
email = Data.generate_email()
print(email)  # "john.smith@example.com"
```

#### generate_phone

```python
Data.generate_phone() -> str
```

Generates a random phone number.

**Example:**
```python
phone = Data.generate_phone()
print(phone)  # "+1-555-123-4567"
```

### Authentication Data

#### generate_auth_user

```python
Data.generate_auth_user() -> Dict[str, str]
```

Generates a complete user authentication object with username and password.

**Returns:**
```python
{
    "username": "john_smith_123",
    "password": "SecureP@ssw0rd123"
}
```

**Example:**
```python
user = Data.generate_auth_user()
print(user["username"])  # "john_smith_123"
print(user["password"])  # "SecureP@ssw0rd123"
```

#### generate_password

```python
Data.generate_password() -> str
```

Generates a secure random password.

**Example:**
```python
password = Data.generate_password()
print(password)  # "Kp9$mN2#xR4@"
```

### Identification

#### generate_id

```python
Data.generate_id() -> str
```

Generates a unique UUID.

**Example:**
```python
user_id = Data.generate_id()
print(user_id)  # "f47ac10b-58cc-4372-a567-0e02b2c3d479"
```

### Address Information

#### generate_address

```python
Data.generate_address() -> str
```

Generates a complete postal address.

**Example:**
```python
address = Data.generate_address()
print(address)  # "123 Main St\nAnytown, CA 12345"
```

#### generate_city

```python
Data.generate_city() -> str
```

Generates a random city name.

#### generate_state

```python
Data.generate_state() -> str
```

Generates a random state/province name.

#### generate_zipcode

```python
Data.generate_zipcode() -> str
```

Generates a random postal code.

#### generate_country

```python
Data.generate_country() -> str
```

Generates a random country name.

### Text Content

#### generate_text

```python
Data.generate_text() -> str
```

Generates random text (short paragraph).

**Example:**
```python
text = Data.generate_text()
print(text)  # "Lorem ipsum dolor sit amet..."
```

#### generate_paragraph

```python
Data.generate_paragraph() -> str
```

Generates a longer random paragraph.

### Professional Information

#### generate_job

```python
Data.generate_job() -> str
```

Generates a random job title.

**Example:**
```python
job = Data.generate_job()
print(job)  # "Software Engineer"
```

### Date and Time

#### generate_date

```python
Data.generate_date() -> str
```

Generates a random date in ISO format (YYYY-MM-DD).

#### generate_datetime

```python
Data.generate_datetime() -> str
```

Generates random date and time in ISO format.

#### generate_time

```python
Data.generate_time() -> str
```

Generates a random time.

### URL and Network

#### generate_url

```python
Data.generate_url() -> str
```

Generates a random URL.

**Example:**
```python
url = Data.generate_url()
print(url)  # "https://www.example.com/page"
```

#### generate_domain

```python
Data.generate_domain() -> str
```

Generates a random domain name.

**Example:**
```python
domain = Data.generate_domain()
print(domain)  # "example.com"
```

#### generate_ipv4

```python
Data.generate_ipv4() -> str
```

Generates a random IPv4 address.

**Example:**
```python
ip = Data.generate_ipv4()
print(ip)  # "192.168.1.1"
```

### Company Information

#### generate_company

```python
Data.generate_company() -> str
```

Generates a random company name.

#### generate_company_email

```python
Data.generate_company_email() -> str
```

Generates a random company email address.

**Example:**
```python
email = Data.generate_company_email()
print(email)  # "info@example.com"
```

### Product Information

#### generate_product_name

```python
Data.generate_product_name() -> str
```

Generates a random product name.

#### generate_price

```python
Data.generate_price(min_price: float = 1.0, max_price: float = 1000.0) -> str
```

Generates a random price.

**Parameters:**
- `min_price` (float): Minimum price value. Default is 1.0.
- `max_price` (float): Maximum price value. Default is 1000.0.

**Example:**
```python
price = Data.generate_price()
print(price)  # "99.99"

price = Data.generate_price(min_price=10.0, max_price=500.0)
print(price)  # "249.50"
```

### Bulk Generation

#### generate_users

```python
Data.generate_users(
    count: int = 1,
    fields: list[str] | None = None
) -> list[dict[str, str]]
```

Generates a list of users.

**Parameters:**
- `count` (int): Number of users to generate. Default is 1.
- `fields` (list[str] | None): Fields to include. Available: 'id', 'name', 'username', 'password', 'email', 'age', 'address', 'phone', 'city', 'state', 'country', 'company'. If None, generates all fields.

**Example:**
```python
users = Data.generate_users(5)
print(users)  # [{'id': '...', 'name': '...', ...}, ...]

users = Data.generate_users(3, fields=['name', 'email'])
print(users)  # [{'name': '...', 'email': '...'}, ...]
```

#### generate_companies

```python
Data.generate_companies(count: int = 1) -> list[dict[str, str]]
```

Generates a list of companies.

**Parameters:**
- `count` (int): Number of companies to generate. Default is 1.

**Example:**
```python
companies = Data.generate_companies(3)
print(companies)  # [{'name': '...', 'email': '...', ...}, ...]
```

#### generate_products

```python
Data.generate_products(
    count: int = 1,
    include_price: bool = True
) -> list[dict[str, str]]
```

Generates a list of products.

**Parameters:**
- `count` (int): Number of products to generate. Default is 1.
- `include_price` (bool): Include random price. Default is True.

**Example:**
```python
products = Data.generate_products(5)
print(products)  # [{'name': '...', 'price': '...'}, ...]

products = Data.generate_products(3, include_price=False)
print(products)  # [{'name': '...'}, ...]
```

### Locale Management

#### set_locale

```python
Data.set_locale(locale: str) -> None
```

Sets the locale for data generation.

**Parameters:**
- `locale` (str): Locale code (e.g., 'es_ES', 'en_US', 'fr_FR', 'de_DE').

**Example:**
```python
Data.set_locale("es_ES")
print(Data.generate_name())  # "Carlos García"

Data.set_locale("en_US")
print(Data.generate_name())  # "John Smith"
```

#### reset_locale

```python
Data.reset_locale() -> None
```

Resets Faker to default locale (en_US).

**Example:**
```python
Data.set_locale("es_ES")
Data.reset_locale()
print(Data.generate_name())  # "John Smith"
```

## Complete Example

```python
from rapidtest import HTTPTest, Data

# Initialize API tester
api = HTTPTest(url="http://localhost:8000")

# Generate fake user data
fake_user = {
    "id": Data.generate_id(),
    "username": Data.generate_name().replace(" ", "_").lower(),
    "email": Data.generate_email(),
    "password": Data.generate_password(),
    "phone": Data.generate_phone(),
    "address": Data.generate_address(),
    "job": Data.generate_job()
}

# Use fake data in API test
response = api.post(
    path="/users",
    json=fake_user,
    status=201
)

# Generate auth user for login tests
auth_user = Data.generate_auth_user()
api.post(
    path="/login",
    json=auth_user,
    status=200
)

# Generate multiple users for testing
users = Data.generate_users(10, fields=['name', 'email'])
for user in users:
    api.post(path="/users", json=user, status=201)
```

## Benefits

- **Realistic Data**: Uses the Faker library for realistic fake data
- **No Hardcoding**: Avoid hardcoded test values that may become stale
- **Variety**: Each test run uses different data, improving test coverage
- **Convenience**: Simple static methods for quick data generation
- **Locale Support**: Generate data in different languages and regions