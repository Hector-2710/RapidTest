# Quick Start

Get up and running with RapidTest in just a few minutes!

## 1. Initialize RapidTest

```python
from rapidtest import Test

# Configure your API's base URL
tester = Test(url="http://localhost:8000")
```

## 2. Basic HTTP Methods

### GET Request

```python
# Simple GET request
tester.get(endpoint="/users", expected_status=200)
```

### POST Request

```python
# POST with JSON data
user_data = {"username": "hector", "password": "123"}
tester.post(
    endpoint="/user", 
    json=user_data, 
    expected_status=201, 
    expected_body=user_data
)
```

### Other HTTP Methods

```python
# PUT request
tester.put(endpoint="/user/1", json={"name": "Updated Name"})

# PATCH request  
tester.patch(endpoint="/user/1", json={"email": "new@email.com"})

# DELETE request
tester.delete(endpoint="/user/1", expected_status=204)
```

## 3. Response Validation

### Status Code Validation

```python
# Expect specific status code
tester.get(endpoint="/users", expected_status=200)
```

### Response Body Validation

```python
expected_response = {"id": 1, "name": "John"}
tester.get(
    endpoint="/users/1", 
    expected_status=200,
    expected_body=expected_response
)
```

## 4. Error Handling

RapidTest provides clear, colorized output when tests fail:

- ✅ Green for successful tests
- ❌ Red for failed tests  
- 📊 Detailed error information

## What's Next?

- Explore [Advanced Examples](../tutorial/advanced-examples.md)
- Learn about [Performance Testing](../api/performance.md)
- Check out our [API Reference](../api/rapidtest.md)