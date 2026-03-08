![RapidTest Logo](docs/images/RapidTest-logo.png)

# RapidTest 🚀

A **super lightweight** and blazingly fast library to simplify REST API testing. Designed to be intuitive, fast to implement.

## ✨ Features

- **Simplicity**: Perform HTTP requests (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`) in a single line with comprehensive response validation.
- **Automatic Validation**: Automatically compare status codes and response bodies with detailed error reporting.
- **Data Generator**: Integrated random data generator (using Faker) for dynamic testing with flexible user creation.
- **Performance Testing**: Built-in load testing with threading - no external tools needed!

## 🛠️ Installation

Install the required dependencies:

```bash
pip install rapidtest
```

## 🚀 Quick Start

### 1. Initialize RapidTest

```python
from rapidtest import Test

# Configure your API's base URL
tester = Test(url="http://localhost:8000")
```

### 2. Run Tests

#### GET
```python
tester.get(endpoint="/users", expected_status=200)
```

#### POST with Body Validation
```python
user_data = {"username": "Uziel", "password": "Mypass123"}
tester.post(endpoint="/user", json=user_data, expected_status=201, expected_json=user_data)
```

### Advanced Example with Dynamic Data

```python
from rapidtest import Test, data

# Initialize tester
tester = Test(url="http://127.0.0.1:8000")

# Generate dynamic test data
user = data.generate_user(id=True, name=True, email=True, age=True, password=True, username=True)

# Test user creation
tester.post(endpoint="/user", json=user, expected_status=201)
```

### 3. Generate Random Data

Use the `data` class to create test data on the fly:

```python
from rapidtest import data

# Generate specific data types
auth_user = data.generate_auth_user()
email = data.generate_email()
name = data.generate_name()
phone = data.generate_phone()

print(auth_user) # {'username': '...', 'password': '...'}
```

### Additional Parameters

All HTTP methods support additional parameters:

```python
# Query parameters
tester.get(endpoint="/users", params={"page": 1, "limit": 10})

# Custom headers
tester.post(endpoint="/auth", json=user_data, headers={"Content-Type": "application/json"})
```

## ⚡ RapidTest vs FastAPI TestClient

See the difference yourself! RapidTest dramatically simplifies your testing code:

### 📋 FastAPI's TestClient Approach
```python
# Traditional FastAPI TestClient - More verbose
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_read_item():
    response = client.get("/items/foo")
    assert response.status_code == 200
    assert response.json() == {"id": "foo", "title": "Foo"}

# Result: 4 lines for the test
```

### 🚀 RapidTest Approach  
```python
# RapidTest - Clean and concise
from rapidtest import Test

fastTest = Test(url="http://localhost:8000")
fastTest.get(endpoint="/items/foo", expected_status=200, expected_json={"id": "foo", "title": "Foo"})

# Result: 2 lines for the test
```

### 🎯 Key Advantages

| Feature | FastAPI TestClient | RapidTest |
|---------|-------------------|-----------|
| **Lines of code** | 4+ lines | 2 lines |
| **Assertions** | Manual `assert` statements | Built-in validation |
| **Setup complexity** | Import app, create client | Simple URL configuration |
| **Error reporting** | Basic assertion errors | Detailed, colored output |
| **Data generation** | Manual or external tools | Built-in `data` class |
| **Performance testing** | Requires additional tools | Built-in `Performance` class |

**Result: 50% less code, 100% more clarity!** ✨

## 🚀 Performance Testing

Use the `Performance` class to run simple load tests on your APIs:
Beta*

```python
from rapidtest import Performance

# Initialize performance test
perf = Performance(
    base_url="http://localhost:8000",
    users=10,       # Number of concurrent users
    duration=30,    # Test duration in seconds  
    timeout=10      # Request timeout
)

# Add endpoint to test
perf.add_get_task(endpoint="/api/users")

# Run the test and shown results in terminal)
perf.run()
```

### Performance Test Output

See real results in action:

![Performance Test Results](docs/images/performance_results.png)


## 📊 Reports

See how your tests look with real colorized output:

### ✅ Successful Test
![Test Passed](docs/images/test_passed.png)

### ❌ Failed Test
![Test Failed](docs/images/test_failed.png)

## 📁 Project Structure

- `rapidtest/`
  - `RapidTest.py`: Core library logic with comprehensive API testing methods and detailed response handling
  - `RapidData.py`: Random data generator with flexible user creation and comprehensive fake data
  - `Performance.py`: Simple performance testing (no external deps)
  - `Utils.py`: Formatting and reporting utilities
  - `__init__.py`: Module configuration

## 🔧 Dependencies

- `requests>=2.25.1`: For making HTTP requests
- `faker>=13.0.0`: For generating fake data

## 📋 Requirements

- Python >=3.7

## 📖 Project Information

- **Version**: 0.3.3
- **Author**: Hector Rosales
- **License**: MIT
- **Homepage**: https://github.com/hector-dev/rapidtest

---
⚡ **Built for speed and simplicity** - because testing should be fast and fun! 🛠️✨
