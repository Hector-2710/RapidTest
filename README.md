# FastTest 🚀

A lightweight and simple library to simplify REST API testing. Designed to be intuitive, fast to implement, and with clear visual reports.

## ✨ Features

- **Simplicity**: Perform HTTP requests (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`) in a single line.
- **Automatic Validation**: Automatically compare status codes and response bodies.
- **Visual Reports**: Formatted console output with colors to identify failures quickly.
- **FastData**: Integrated random data generator (using Faker) for dynamic testing.

## 🛠️ Installation

Make sure you have the necessary dependencies installed:

```bash
pip install requests faker
```

## 🚀 Quick Start

### 1. Initialize FastTest

```python
from FastTest import FastTest

# Configure your API's base URL
tester = FastTest("http://localhost:8000")
```

### 2. Run Tests

#### GET
```python
tester.get("/users", expected_status=200)
```

#### POST with Body Validation
```python
user_data = {"username": "hector", "password": "123"}
tester.post("/user", data=user_data, expected_status=201, expected_body=user_data)
```

#### PUT / PATCH / DELETE
```python
# Update data
tester.put("/user/hector", data={"password": "new_password"}, expected_status=200)

# Delete resource
tester.delete("/user/hector", expected_status=200)
```

### 3. Generate Random Data (FastData)

Use `FastData` to create test data on the fly:

```python
from FastData import FastData

user = FastData.generate_auth_user()
email = FastData.generate_email()

print(user) # {'username': '...', 'password': '...'}
```

## 📊 Reports

Each test generates a visual report in the console like this:

```text
============================================================
 TEST PASSED 
============================================================
URL:    http://localhost:8000/user
Status: 201
Body:
{
    "username": "hector",
    "password": "123"
}
============================================================
```

## 📁 Project Structure

- `FastTest.py`: Core library logic.
- `FastData.py`: Random data generator.
- `utils.py`: Formatting and reporting utilities.

---
Built to simplify a developer's life. Happy testing! 🛠️
