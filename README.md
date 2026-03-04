![RapidTest Logo](docs/images/RapidTest-logo.png)

# RapidTest 🚀

A **super lightweight** and blazingly fast library to simplify REST API testing. Designed to be intuitive, fast to implement, and with clear colorized reports - **no heavy dependencies!**

## ✨ Features

- **Simplicity**: Perform HTTP requests (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`) in a single line with comprehensive response validation.
- **Automatic Validation**: Automatically compare status codes and response bodies with detailed error reporting.
- **Fast & Lightweight**: Minimal dependencies, maximum speed!
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

#### PATCH / PUT / DELETE
```python
# Update data
tester.patch(endpoint="/user/hector", json={"password": "new_password"}, expected_status=200)

# Delete resource  
tester.delete(endpoint="/user/hector", expected_status=204)
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

# Test user retrieval 
tester.get(endpoint=f"/users/{user['email']}", expected_status=200)

# Test user update
tester.put(endpoint=f"/user/{user['id']}", json=user, expected_status=200)

# Test user deletion
tester.delete(endpoint=f"/user/{user['id']}", expected_status=202)
```

### 3. Generate Random Data

Use the `data` class to create test data on the fly:

```python
from rapidtest import data

# Generate a complete user with all fields
user = data.generate_user(id=True, name=True, email=True, age=True, password=True, username=True)
print(user) # {'id': '...', 'name': '...', 'email': '...', 'age': '25', 'password': '...', 'username': '...'}

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

# Form data
tester.post(endpoint="/upload", data={"file": "content"})

# Additional requests arguments
tester.get(endpoint="/secure", timeout=30, verify=False)
```

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

### Simple Performance Testing Features

- **No external dependencies**: Uses only `requests` and `threading`
- **Real-time terminal output**: See results as they happen
- **Basic load simulation**: Multiple concurrent users
- **Essential metrics**: Response times, success rates, RPS

### Performance Test Output

See real results in action:

![Performance Test Results](docs/images/performance_results.png)


## 📊 Reports

See how your tests look with real colorized output:

### ✅ Successful Test
![Test Passed](docs/images/test_passed.png)

### ❌ Failed Test
![Test Failed](docs/images/test_failed.png)

**Colors:**
- ✅ Green for PASSED tests
- ❌ Red for FAILED tests  
- 🔵 Blue for labels and info
- 🟡 Yellow for warnings

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

- **Version**: 0.3.2
- **Author**: Hector Rosales
- **License**: MIT
- **Homepage**: https://github.com/hector-dev/rapidtest

---
⚡ **Built for speed and simplicity** - because testing should be fast and fun! 🛠️✨
