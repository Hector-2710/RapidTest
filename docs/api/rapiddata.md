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

## Complete Example

```python
from rapidtest import Test, Data

# Initialize API tester
tester = Test(url="http://localhost:8000")

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
response = tester.post(
    endpoint="/users",
    json=fake_user,
    expected_status=201
)

# Generate auth user for login tests
auth_user = Data.generate_auth_user()
tester.post(
    endpoint="/login",
    json=auth_user,
    expected_status=200
)
```

## Benefits

- **Realistic Data**: Uses the Faker library for realistic fake data
- **No Hardcoding**: Avoid hardcoded test values that may become stale
- **Variety**: Each test run uses different data, improving test coverage
- **Convenience**: Simple static methods for quick data generation