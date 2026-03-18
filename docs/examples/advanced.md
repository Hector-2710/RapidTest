# Advanced Examples

This section demonstrates advanced usage patterns and real-world testing scenarios.

## Complete CRUD Testing

```python
from rapidtest import Test, data

# Initialize API client
api = Test(url="http://localhost:8000")

# Generate test data
user_data = {
    "username": data.generate_name().replace(" ", "_").lower(),
    "email": data.generate_email(),
    "password": data.generate_password()
}

print("🧪 Testing CRUD operations...")

# CREATE - Post new user
response = api.post(
    path="/api/users",
    json=user_data,
    status=201
)
user_id = response.json()["id"]

# READ - Get user by ID
api.get(
    path=f"/api/users/{user_id}",
    status=200,
    expected_json={
        "id": user_id,
        "username": user_data["username"],
        "email": user_data["email"]
    }
)

# UPDATE - Modify user
updated_data = {"email": data.generate_email()}
api.patch(
    path=f"/api/users/{user_id}",
    json=updated_data,
    status=200
)

# DELETE - Remove user
api.delete(
    path=f"/api/users/{user_id}",
    status=204
)
```

## Authentication Flow Testing

```python
from rapidtest import Test, data

api = Test(url="http://localhost:8000")

# 1. Register new user
auth_user = data.generate_auth_user()
register_data = {
    "username": auth_user["username"],
    "password": auth_user["password"],
    "email": data.generate_email()
}

api.post(
    path="/auth/register",
    json=register_data,
    status=201
)

# 2. Login with credentials
login_response = api.post(
    path="/auth/login",
    json={
        "username": auth_user["username"],
        "password": auth_user["password"]
    },
    status=200
)

# Extract token from response
token = login_response.json()["token"]

# 3. Access protected endpoint
api.get(
    path="/auth/profile",
    headers={"Authorization": f"Bearer {token}"},
    status=200
)
```

## Testing with Dynamic Data

```python
from rapidtest import Test, data

api = Test(url="http://localhost:8000")

# Test multiple users with generated data
for i in range(5):
    user = {
        "id": data.generate_id(),
        "name": data.generate_name(),
        "email": data.generate_email(),
        "phone": data.generate_phone(),
        "address": data.generate_address(),
        "job": data.generate_job()
    }
    
    print(f"Testing user {i+1}: {user['name']}")
    
    api.post(
        path="/users",
        json=user,
        status=201,
        expected_json=user
    )
```

## API Versioning Tests

```python
from rapidtest import Test

# Test multiple API versions
base_url = "http://localhost:8000"
test_data = {"name": "Test Item"}

# Version 1
api_v1 = Test(url=f"{base_url}/api/v1")
api_v1.post(path="/items", json=test_data, status=201)

# Version 2  
api_v2 = Test(url=f"{base_url}/api/v2")
api_v2.post(path="/items", json=test_data, status=201)
```

## Error Handling and Edge Cases

```python
from rapidtest import Test

api = Test(url="http://localhost:8000")

# Test validation errors
invalid_inputs = [
    {"email": "invalid-email"},  # Invalid email format
    {"age": -5},                 # Negative age
    {},                          # Empty payload
    {"username": "a" * 1000}     # Too long username
]

for invalid_data in invalid_inputs:
    api.post(
        path="/users",
        json=invalid_data,
        status=400
    )

# Test authorization errors
api.get(path="/admin/users", status=401)  # No auth header

api.get(
    path="/admin/users", 
    headers={"Authorization": "Bearer invalid-token"},
    status=403  # Invalid token
)
```

## Performance Testing Integration

```python
from rapidtest import Test, Performance, Data

# Regular functional test first
api = Test(url="http://localhost:8000")
test_user = data.generate_auth_user()

# Ensure endpoint works functionally
api.post(path="/auth/login", json=test_user, status=200)

# Then performance test the same endpoint
perf = Performance(
    base_url="http://localhost:8000",
    users=50,
    duration=30,
    timeout=10
)
perf.add_get_task(path="/health")
results = perf.run()

# Validate performance criteria
if results['success_rate'] < 95:
    print("❌ Performance test failed - success rate too low")
    
if results['avg_response_time'] > 1000:
    print("❌ Performance test failed - response time too high")
```

## Pagination Testing

```python
from rapidtest import Test

api = Test(url="http://localhost:8000")

# Test first page
page1 = api.get(
    path="/users",
    params={"page": 1, "limit": 10},
    status=200
)

# Verify pagination structure
response_data = page1.json()
assert "data" in response_data
assert "pagination" in response_data
assert len(response_data["data"]) <= 10

# Test subsequent pages
api.get(
    path="/users",
    params={"page": 2, "limit": 10},
    status=200
)

# Test edge cases
api.get(
    path="/users",
    params={"page": 999, "limit": 10},
    status=200  # Should return empty array
)
```

## File Upload Testing

```python
from rapidtest import Test

api = Test(url="http://localhost:8000")

# Test file upload
with open("test_file.txt", "w") as f:
    f.write("Test file content")

# Upload file using data parameter
with open("test_file.txt", "rb") as f:
    api.post(
        path="/upload",
        data={"file": f},
        status=201
    )
```

## ASGI Direct Testing

Test your FastAPI, Starlette, or any ASGI-compatible application directly without running a real HTTP server. This is faster and doesn't require port binding.

```python
from rapidtest import Test
from myapp.main import app  # Your ASGI app instance

# Initialize in ASGI mode
api = Test(app=app, asgi_mode=True)

# Requests are made directly to the app
api.get(path="/health", status=200)

api.post(
    path="/users",
    json={"name": "ASGI User", "email": "asgi@example.com"},
    status=201
)
```

## Environment-Based Testing

```python
import os
from rapidtest import Test

# Configure based on environment
env = os.getenv("ENV", "local")

if env == "local":
    base_url = "http://localhost:8000"
elif env == "staging":
    base_url = "https://staging-api.example.com"
else:
    base_url = "https://api.example.com"

api = Test(url=base_url)

# Run the same tests across environments
api.get(path="/health", status=200)
```

## Custom Test Runner

```python
from rapidtest import Test, data
import sys

class APITestSuite:
    def __init__(self, base_url):
        self.api = Test(url=base_url)
        self.passed = 0
        self.failed = 0
    
    def run_test(self, test_name, test_func):
        """Run a single test and track results."""
        print(f"🧪 Running: {test_name}")
        try:
            test_func()
            self.passed += 1
            print(f"✅ {test_name} - PASSED")
        except Exception as e:
            self.failed += 1
            print(f"❌ {test_name} - FAILED: {e}")
    
    def test_user_creation(self):
        user = data.generate_auth_user()
        self.api.post(path="/users", json=user, status=201)
    
    def test_user_login(self):
        user = data.generate_auth_user()
        self.api.post(path="/login", json=user, status=200)
    
    def execute_all(self):
        """Run all tests and report results."""
        tests = [
            ("User Creation", self.test_user_creation),
            ("User Login", self.test_user_login),
        ]
        
        for test_name, test_func in tests:
            self.run_test(test_name, test_func)
        
        print(f"\n📊 Results: {self.passed} passed, {self.failed} failed")
        return self.failed == 0

# Usage
if __name__ == "__main__":
    suite = APITestSuite("http://localhost:8000")
    success = suite.execute_all()
    sys.exit(0 if success else 1)
```

These examples demonstrate real-world usage patterns that you can adapt to your specific API testing needs.


