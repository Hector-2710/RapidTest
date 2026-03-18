# Data Generation API

Random data generator for testing using the Faker library.

```python
from rapidtest import data
```

## Data Class

Static class providing fake data generation methods for testing purposes.

### Personal Information

#### generate_name

```python
data.generate_name() -> str
```

Generates a random full name.

**Example:**
```python
name = data.generate_name()
print(name)  # "John Smith"
```

#### generate_email

```python
data.generate_email() -> str
```

Generates a random email address.

**Example:**
```python
email = data.generate_email()
print(email)  # "john.smith@example.com"
```

#### generate_phone

```python
data.generate_phone() -> str
```

Generates a random phone number.

**Example:**
```python
phone = data.generate_phone()
print(phone)  # "+1-555-123-4567"
```

### Authentication Data

#### generate_auth_user

```python
data.generate_auth_user() -> Dict[str, str]
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
user = data.generate_auth_user()
print(user["username"])  # "john_smith_123"
print(user["password"])  # "SecureP@ssw0rd123"
```

#### generate_password

```python
data.generate_password() -> str
```

Generates a secure random password.

**Example:**
```python
password = data.generate_password()
print(password)  # "Kp9$mN2#xR4@"
```

### Identification

#### generate_id

```python
data.generate_id() -> str
```

Generates a unique UUID.

**Example:**
```python
user_id = data.generate_id()
print(user_id)  # "f47ac10b-58cc-4372-a567-0e02b2c3d479"
```

### Address Information

#### generate_address

```python
data.generate_address() -> str
```

Generates a complete postal address.

**Example:**
```python
address = data.generate_address()
print(address)  # "123 Main St\nAnytown, CA 12345"
```

#### generate_city

```python
data.generate_city() -> str
```

Generates a random city name.

#### generate_state

```python
data.generate_state() -> str
```

Generates a random state/province name.

#### generate_zipcode

```python
data.generate_zipcode() -> str
```

Generates a random postal code.

#### generate_country

```python
data.generate_country() -> str
```

Generates a random country name.

### Text Content

#### generate_text

```python
data.generate_text() -> str
```

Generates random text (short paragraph).

**Example:**
```python
text = data.generate_text()
print(text)  # "Lorem ipsum dolor sit amet..."
```

#### generate_paragraph

```python
data.generate_paragraph() -> str
```

Generates a longer random paragraph.

### Professional Information

#### generate_job

```python
data.generate_job() -> str
```

Generates a random job title.

**Example:**
```python
job = data.generate_job()
print(job)  # "Software Engineer"
```

### Date and Time

#### generate_date

```python
data.generate_date() -> str
```

Generates a random date in ISO format (YYYY-MM-DD).

#### generate_datetime

```python
data.generate_datetime() -> str
```

Generates random date and time in ISO format.

#### generate_time

```python
data.generate_time() -> str
```

Generates a random time.

## Complete Example

```python
from rapidtest import Test, data

# Initialize API tester
tester = Test(url="http://localhost:8000")

# Generate fake user data
fake_user = {
    "id": data.generate_id(),
    "username": data.generate_name().replace(" ", "_").lower(),
    "email": data.generate_email(),
    "password": data.generate_password(),
    "phone": data.generate_phone(),
    "address": data.generate_address(),
    "job": data.generate_job()
}

# Use fake data in API test
response = tester.post(
    endpoint="/users",
    json=fake_user,
    status=201
)

# Generate auth user for login tests
auth_user = data.generate_auth_user()
tester.post(
    endpoint="/login",
    json=auth_user,
    status=200
)
```

## Benefits

- **Realistic Data**: Uses the Faker library for realistic fake data
- **No Hardcoding**: Avoid hardcoded test values that may become stale
- **Variety**: Each test run uses different data, improving test coverage
- **Convenience**: Simple static methods for quick data generation