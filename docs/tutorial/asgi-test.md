# Tutorial: ASGI Testing

Learn how to test ASGI applications directly, without needing to start an HTTP server. This makes tests faster and easier to set up.

## What is ASGI Testing?

`ASGITest` allows you to test your application (FastAPI, Starlette, etc.) directly by running it in memory, without needing to start a server.

**Advantages:**
- ⚡ Faster - no server needed
- 🔧 Easier to configure
- 🧪 Ideal for unit tests
- 🎯 Works with any ASGI app

## Initial Setup

```python
from rapidtest import ASGITest
from your_app import app  # Your FastAPI/Starlette app

# Initialize the tester with your app
api = ASGITest(app=app)
```

## Available HTTP Methods

The same methods as HTTPTest are available:

### GET

```python
# Basic request
api.get(path="/", status=200)

# With parameters
api.get(path="/users", params={"page": 1}, status=200)

# With headers
api.get(
    path="/health",
    headers={"X-Custom": "value"},
    status=200
)

# Validate JSON response
api.get(
    path="/users/1",
    expected_json={"id": 1, "name": "John"},
    status=200
)
```

### POST

```python
# Send JSON
api.post(
    path="/users",
    json={"name": "Jane", "email": "jane@example.com"},
    status=201
)

# With form data
api.post(
    path="/login",
    data={"username": "john", "password": "secret"},
    status=200
)
```

### PUT, PATCH, DELETE

```python
# PUT - Full replacement
api.put(
    path="/users/1",
    json={"name": "Updated", "email": "updated@example.com"},
    status=200
)

# PATCH - Partial update
api.patch(
    path="/users/1",
    json={"name": "New Name"},
    status=200
)

# DELETE - Remove
api.delete(path="/users/1", status=204)
```

## Complete Example: FastAPI Testing

### Your application (app.py)

```python
# app.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"id": user_id, "name": f"User {user_id}"}

@app.post("/users")
def create_user(user: dict):
    user["id"] = 1
    return user
```

### Tests with ASGITest

```python
# test_app.py
from fastapi import FastAPI
from rapidtest import ASGITest

# Create the app
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"id": user_id, "name": f"User {user_id}"}

@app.post("/users")
def create_user(user: dict):
    user["id"] = 1
    return user

# === TESTS ===

api = ASGITest(app=app)

print("1. Testing health endpoint...")
api.get(path="/health", status=200, keys=["status"])

print("\n2. Testing user detail...")
api.get(path="/users/5", status=200, expected_json={"id": 5, "name": "User 5"})

print("\n3. Testing user creation...")
api.post(
    path="/users",
    json={"name": "John", "email": "john@example.com"},
    status=201,
    keys=["id"]
)

print("\n4. Testing root endpoint...")
api.get(path="/", status=200, expected_json={"message": "Hello World"})

# Close the event loop at the end
api.close()
```

## Differences between HTTPTest and ASGITest

| Aspect | HTTPTest | ASGITest |
|--------|----------|----------|
| **Server** | Requires running server | No server required |
| **Speed** | Slower | Faster |
| **Use case** | Integration tests | Unit tests |
| **Config** | Needs server URL | Only the app |
| **Import** | `from rapidtest import HTTPTest` | `from rapidtest import ASGITest` |

## Integration with pytest

```python
# conftest.py
import pytest
from fastapi import FastAPI
from rapidtest import ASGITest

@pytest.fixture
def app():
    return FastAPI()

@pytest.fixture
def api(app):
    tester = ASGITest(app=app)
    yield tester
    tester.close()

# test_api.py
def test_health(api):
    api.get(path="/health", status=200)

def test_create_user(api):
    api.post(
        path="/users",
        json={"name": "Test"},
        status=201
    )
```

## Error Handling

```python
from fastapi import FastAPI, HTTPException
from rapidtest import ASGITest

app = FastAPI()

@app.get("/item/{item_id}")
def get_item(item_id: int):
    if item_id == 404:
        raise HTTPException(status_code=404, detail="Not found")
    return {"id": item_id}

api = ASGITest(app=app)

# Test 404 error
api.get(path="/item/404", status=404)
```

## Important Notes

1. **Close resources**: After finishing tests, call `api.close()` to close the event loop.

2. **ASGI Scope**: The created scope is basic "http" type. If your app depends on WebSockets or other advanced features, it may not work the same.

3. **Headers**: Headers are automatically converted to lowercase (per ASGI specification).

## Next Step

Need to do load testing? Learn about [Performance Testing](performance.md).