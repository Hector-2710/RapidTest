# Tutorial: HTTP Testing

Learn how to test traditional HTTP APIs with `HTTPTest`. This class is ideal when you need to test a server that's already running.

## Requirements

- A running API server (local or remote)
- Install RapidTest: `pip install rapidtest`

## Initial Setup

```python
from rapidtest import HTTPTest

# Connect to your API
api = HTTPTest(url="http://localhost:8000", timeout=30)
```

## Available HTTP Methods

### GET - Retrieve data

```python
# Basic request
api.get(path="/users", status=200)

# With query parameters
api.get(
    path="/users",
    params={"page": 1, "limit": 10},
    status=200
)

# With headers
api.get(
    path="/protected",
    headers={"Authorization": "Bearer token123"},
    status=200
)

# Validate JSON response
api.get(
    path="/users/1",
    expected_json={"id": 1, "name": "John"},
    status=200
)

# Validate that response contains certain keys
api.get(
    path="/users/1",
    keys=["id", "name", "email"],
    status=200
)
```

### POST - Create resources

```python
# Send JSON
new_user = {"name": "Jane", "email": "jane@example.com"}
api.post(
    path="/users",
    json=new_user,
    status=201
)

# Send form data
api.post(
    path="/login",
    data={"username": "john", "password": "secret"},
    status=200
)

# With response validation
api.post(
    path="/users",
    json={"name": "Jane"},
    status=201,
    expected_json={"id": 1, "name": "Jane"}
)
```

### PUT - Replace resources

```python
# Full update
api.put(
    path="/users/1",
    json={"name": "John Updated", "email": "john@example.com"},
    status=200
)
```

### PATCH - Partial update

```python
# Partial update
api.patch(
    path="/users/1",
    json={"email": "newemail@example.com"},
    status=200
)
```

### DELETE - Delete resources

```python
# Delete a resource
api.delete(path="/users/1", status=204)
```

## Complete Example: User CRUD

```python
from rapidtest import HTTPTest, Data

api = HTTPTest(url="http://localhost:8000")

# CREATE - Create user
new_user = {
    "name": Data.generate_name(),
    "email": Data.generate_email(),
    "age": 25
}
response = api.post(path="/users", json=new_user, status=201)
user_id = response.json()["id"]
print(f"User created: {user_id}")

# READ - Get user
api.get(path=f"/users/{user_id}", status=200)

# UPDATE - Update user
api.patch(
    path=f"/users/{user_id}",
    json={"name": "New Name"},
    status=200
)

# DELETE - Delete user
api.delete(path=f"/users/{user_id}", status=204)
```

## Error Handling

```python
from rapidtest import HTTPTest

api = HTTPTest(url="http://localhost:8000")

# Test common errors
api.get(path="/users/999999", status=404)  # Not found

api.post(
    path="/users",
    json={"email": "invalid-email"},  # Invalid email
    status=400  # Bad Request
)

api.get(path="/admin", status=401)  # Unauthorized
```

## Integration with unittest

```python
import unittest
from rapidtest import HTTPTest

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.api = HTTPTest(url="http://localhost:8000")
    
    def test_health_check(self):
        self.api.get(path="/health", status=200)
    
    def test_create_user(self):
        response = self.api.post(
            path="/users",
            json={"name": "Test"},
            status=201
        )
        self.assertIsNotNone(response)

if __name__ == "__main__":
    unittest.main()
```

## Parameters Summary

| Parameter | Description | Example |
|-----------|-------------|---------|
| `path` | API endpoint | `/users/1` |
| `status` | Expected status code | `200`, `201`, `404` |
| `expected_json` | Exact JSON expected in response | `{"id": 1}` |
| `keys` | Keys that must exist in response | `["id", "name"]` |
| `params` | Query parameters | `{"page": 1}` |
| `headers` | HTTP headers | `{"Auth": "Bearer..."}` |
| `json` | JSON body for POST/PUT/PATCH | `{"name": "John"}` |
| `data` | Form data | `{"user": "john"}` |

## Next Step

Need to test your app directly without starting a server? Learn about [ASGITest](asgi-test.md).