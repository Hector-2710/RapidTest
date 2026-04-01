# 🚀 Quick Start

Get up and running with RapidTest in just a few minutes! ⚡

## 1. 🔧 Initialize RapidTest

```python
from rapidtest import Test

# Configure your API's base URL
tester = Test(url="http://localhost:8000")
```

Or initialize a starter file with the CLI:

```bash
rapidtest init
```

## 2. 🌐 Basic HTTP Methods

### 📥 GET Request

```python
# Simple GET request
tester.get(path="/users", status=200)
```

### 📤 POST Request

```python
# POST with JSON data
user_data = {"username": "hector", "password": "123"}
tester.post(
    path="/user", 
    json=user_data, 
    status=201, 
    expected_json=user_data
)
```

### 🔄 Other HTTP Methods

```python
# PUT request
tester.put(path="/user/1", json={"name": "Updated Name"})

# PATCH request  
tester.patch(path="/user/1", json={"email": "new@email.com"})

# DELETE request
tester.delete(path="/user/1", status=204)
```

### ⚡ ASGI mode with the same class

```python
from rapidtest import Test
from backend.main import app

tester = Test(app=app, asgi_mode=True)
tester.get(path="/health", status=200)
```

## 3. ✅ Response Validation

### 🎯 Status Code Validation

```python
# Expect specific status code
tester.get(path="/", status=200)
```

### 📋 Response Body Validation

```python
tester.get(
    path="/", 
    status=200,
    expected_json= "API running"
)
```

> **💡 NOTE:** 
Remember that the expected_json will depend solely on how the endpoint is defined.

## 4. 🚨 Error Handling

RapidTest provides clear, colorized output when tests fail:

- ✅ Green for successful tests
- ❌ Red for failed tests  
- 📊 Detailed error information

## 🎯 What's Next?

- ⚡ Learn about [HTTP Methods](../learn/http-methods.md)
- 📚 Check out our [API Reference](../api/rapidtest.md)