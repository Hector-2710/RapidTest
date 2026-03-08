# Basic Guide: From Your API to Performance Testing

Welcome! This guide will walk you step by step through the complete API testing process, from initial setup to performance analysis. Imagine you've just developed an API and want to ensure everything works perfectly.

## 🚀 Step 1: You Have Your API with Endpoints

First, let's understand the situation: **you already have a working API** with several endpoints. For example, suppose your API has these typical endpoints:

- `GET /health` - To verify that the server is running
- `GET /users` - To get the list of users
- `POST /users` - To create a new user
- `GET /users/{id}` - To get a specific user
- `PUT /users/{id}` - To update a user
- `DELETE /users/{id}` - To delete a user

These are common endpoints in any REST API. Now you need to **test that they work correctly** before deploying to production.

## ✅ Step 2: Let's Test these Endpoints to Ensure They Work

This is where RapidTest comes in. We're going to test each endpoint systematically to ensure it responds as we expect.

### Initialize Your Testing Client

First, point RapidTest to your API:

```python
from rapidtest import Test

# Point to your API server (can be local or remote)
tester = Test(url="http://localhost:8000")
```

### Basic Test: Is the Server Running?

The first test should always be to verify that your server responds:

```python
# Verify that your API is running
tester.get(endpoint="/health", expected_status=200)
```

If this works, you'll see: ✅ **GET /health** - Perfect! Your server is responding.

### Test Read Endpoints (GET)

Now let's test getting data:

```python
# Get the list of users
tester.get(endpoint="/users", expected_status=200)

# If you have users, test getting a specific one
tester.get(endpoint="/users/1", expected_status=200)
```

### Test Write Endpoints (POST, PUT, DELETE)

Now let's test creating, updating, and deleting data:

```python
# Create a new user
new_user = {
    "username": "test_user",
    "email": "test@example.com",
    "name": "Test User"
}

tester.post(
    endpoint="/users",
    input_json=new_user,
    expected_status=201  
)
```

### Advanced Validation: Not Just Status Code

Often it's not enough to verify that the endpoint responds - we want to verify it returns the **correct data**:

```python
# Verify both status and response content
expected_user = {
    "id": 1,
    "username": "test_user",
    "email": "test@example.com"
}

tester.get(
    endpoint="/users/1",
    expected_status=200,
    expected_body=expected_user
)
```

### Testing Error Scenarios

It's crucial to test that your API handles errors correctly:

```python
# Test that it returns 404 for users that don't exist
tester.get(endpoint="/users/99999", expected_status=404)

# Test validation of invalid data
invalid_data = {"email": "badly-formatted-email"}
tester.post(
    endpoint="/users",
    json=invalid_data,
    expected_status=400  # 400 means "invalid request"
)
```

### Authentication and Headers

If your API requires authentication, you can include headers:

```python
# Testing with authorization token
auth_headers = {"Authorization": "Bearer your-token-here"}

tester.get(
    endpoint="/profile",
    headers=auth_headers,
    expected_status=200
)
```

## 📊 Step 3: Need to Generate Test Data? We've Got Data

Often you need **realistic test data** to properly test your API. RapidTest includes a data generator that helps you create believable information.

### Why Do You Need Test Data?

- **Test with volume**: Your API should work with many records, not just 2 or 3
- **Realistic data**: Real data has specific patterns that random data doesn't capture
- **Edge case testing**: Long names, special characters, etc.

### Generating Realistic User Data

```python
from rapidtest import data

# Generate a realistic user
fake_user = generator.generate_user(name=True, email=True, age=True)
# example: {'name': 'Maria Gonzalez', 'email': 'maria.gonzalez@email.com', 'age': 28}

# Now use this data in your test
tester.post(
    endpoint="/users",
    json=fake_user,
    expected_status=201
)
```

### Creating Multiple Users for Testing

```python
# Generate 10 users to test your API with volume
for i in range(10):
    user = data.generate_user(name=True, email=True, age=True)
    
    # Add each user to your API
    tester.post(
        endpoint="/users",
        input_json=user,
        expected_status=201
    )
```


## ⚡ Step 4: Now You Can Test Performance

Once you know your API works correctly with individual data, it's time to verify **how it behaves under load**. What happens when 10, 50, or 100 users use your API at the same time?

### Why Performance Testing?

- **Identify bottlenecks**: Find the slowest endpoints before your users do
- **Validate capacity**: Make sure your API can handle expected traffic
- **Optimization**: Get real data to improve your API

### Basic Performance Testing

```python
from rapidtest import Performance

# Create a performance tester
perf_tester = Performance(
    base_url="http://localhost:8000",
    users=10,
    duration=20,
    timeout=5
    )

# Simulate 10 concurrent users for 20 seconds
perf_tester.add_get_task(endpoint="/")
perf_tester.run()
```

### Interpreting the Results

RapidTest gives you key metrics to understand performance:

- **RPS (Requests Per Second)**: How many requests your API handles per second
- **Average Response Time**: How fast your API responds
- **Success Rate**: Percentage of requests that complete successfully (without errors)

```python
# Example output
# 🚀 Performance Test Completed
# 📊 Total requests: 487
# ⚡ Requests per second: 16.2
# ⏱️  Average time: 245ms
# ✅ Successes: 485 (99.6%)
# ❌ Errors: 2 (0.4%)
```

## 🎯 Complete Workflow: The Full Process in Action

Here's a complete example that follows the entire process:

```python
from rapidtest import Test, data, Performance

# 1. SETUP: Point to your API
tester = Test(url="http://localhost:8000")
perf_tester = Performance(
    url="http://localhost:8000",
    users=10,
    duration=30,
    timeout=5
    )

print("🔍 Step 1: Verifying that the API responds...")

# 2. FUNCTIONAL TESTING: Verify it works
try:
    tester.get(endpoint="/health", expected_status=200)
    print("✅ API is working correctly")
except:
    print("❌ Error: API not responding")
    exit()

print("\n📊 Step 2: Testing with test data...")

# 3. TEST DATA: Create realistic users
for i in range(5):
    user = data.generate_user(name=True, email=True, age=True)
    tester.post(
        endpoint="/users",
        json=user,
        expected_status=201
        )

print("✅ Test users created successfully")

print("\n⚡ Step 3: Performance testing...")

# 4. PERFORMANCE: Verify under load
perf_tester.add_get_task(endpoint="/")
perf_tester.run()

```