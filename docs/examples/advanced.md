# Advanced Examples

This section demonstrates advanced usage patterns and real-world testing scenarios.

## Complete CRUD Testing

```python
from rapidtest import Test, Data

# Initialize API client
api = Test(url="http://localhost:8000")

# Generate test data
user_data = {
    "username": Data.generate_name().replace(" ", "_").lower(),
    "email": Data.generate_email(),
    "password": Data.generate_password()
}

print("🧪 Testing CRUD operations...")

# CREATE - Post new user
response = api.post(
    endpoint="/api/users",
    json=user_data,
    expected_status=201
)
user_id = response.json()["id"]

# READ - Get user by ID
api.get(
    endpoint=f"/api/users/{user_id}",
    expected_status=200,
    expected_body={
        "id": user_id,
        "username": user_data["username"],
        "email": user_data["email"]
    }
)

# UPDATE - Modify user
updated_data = {"email": Data.generate_email()}
api.patch(
    endpoint=f"/api/users/{user_id}",
    json=updated_data,
    expected_status=200
)

# DELETE - Remove user
api.delete(
    endpoint=f"/api/users/{user_id}",
    expected_status=204
)
```

## Authentication Flow Testing

```python
from rapidtest import Test, Data

api = Test(url="http://localhost:8000")

# 1. Register new user
auth_user = Data.generate_auth_user()
register_data = {
    "username": auth_user["username"],
    "password": auth_user["password"],
    "email": Data.generate_email()
}

api.post(
    endpoint="/auth/register",
    json=register_data,
    expected_status=201
)

# 2. Login with credentials
login_response = api.post(
    endpoint="/auth/login",
    json={
        "username": auth_user["username"],
        "password": auth_user["password"]
    },
    expected_status=200
)

# Extract token from response
token = login_response.json()["token"]

# 3. Access protected endpoint
api.get(
    endpoint="/auth/profile",
    headers={"Authorization": f"Bearer {token}"},
    expected_status=200
)
```

## Testing with Dynamic Data

```python
from rapidtest import Test, Data

api = Test(url="http://localhost:8000")

# Test multiple users with generated data
for i in range(5):
    user = {
        "id": Data.generate_id(),
        "name": Data.generate_name(),
        "email": Data.generate_email(),
        "phone": Data.generate_phone(),
        "address": Data.generate_address(),
        "job": Data.generate_job()
    }
    
    print(f"Testing user {i+1}: {user['name']}")
    
    api.post(
        endpoint="/users",
        json=user,
        expected_status=201,
        expected_body=user
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
api_v1.post(endpoint="/items", json=test_data, expected_status=201)

# Version 2  
api_v2 = Test(url=f"{base_url}/api/v2")
api_v2.post(endpoint="/items", json=test_data, expected_status=201)
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
        endpoint="/users",
        json=invalid_data,
        expected_status=400
    )

# Test authorization errors
api.get(endpoint="/admin/users", expected_status=401)  # No auth header

api.get(
    endpoint="/admin/users", 
    headers={"Authorization": "Bearer invalid-token"},
    expected_status=403  # Invalid token
)
```

## Performance Testing Integration

```python
from rapidtest import Test, Performance, Data

# Regular functional test first
api = Test(url="http://localhost:8000")
test_user = Data.generate_auth_user()

# Ensure endpoint works functionally
api.post(endpoint="/auth/login", json=test_user, expected_status=200)

# Then performance test the same endpoint
perf = Performance(
    base_url="http://localhost:8000",
    users=50,
    duration=30,
    timeout=10
)
perf.add_get_task(endpoint="/health")
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
    endpoint="/users",
    params={"page": 1, "limit": 10},
    expected_status=200
)

# Verify pagination structure
response_data = page1.json()
assert "data" in response_data
assert "pagination" in response_data
assert len(response_data["data"]) <= 10

# Test subsequent pages
api.get(
    endpoint="/users",
    params={"page": 2, "limit": 10},
    expected_status=200
)

# Test edge cases
api.get(
    endpoint="/users",
    params={"page": 999, "limit": 10},
    expected_status=200  # Should return empty array
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
        endpoint="/upload",
        data={"file": f},
        expected_status=201
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
api.get(endpoint="/health", expected_status=200)
```

## Custom Test Runner

```python
from rapidtest import Test, Data
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
        user = Data.generate_auth_user()
        self.api.post(endpoint="/users", json=user, expected_status=201)
    
    def test_user_login(self):
        user = Data.generate_auth_user()
        self.api.post(endpoint="/login", json=user, expected_status=200)
    
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


