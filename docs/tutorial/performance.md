# Tutorial: Performance Testing

Learn how to perform load and stress testing with `Performance`. This class allows you to simulate multiple concurrent users to evaluate your API's performance.

## What is Performance Testing?

RapidTest's `Performance` module allows you to:
- Simulate multiple concurrent users
- Measure response times
- Calculate success rate
- Evaluate throughput (requests per second)

## Initial Setup

```python
from rapidtest import Performance

# Create instance
perf = Performance(
    base_url="http://localhost:8000",
    users=10,        # Concurrent users
    duration=10,    # Duration in seconds
    timeout=10,     # Request timeout
    delay=0.1       # Delay between requests
)
```

## Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `base_url` | str | None | Base URL of the API |
| `users` | int | 10 | Number of concurrent users |
| `duration` | int | 10 | Test duration in seconds |
| `timeout` | int | 10 | Maximum request timeout |
| `delay` | float | 0.1 | Delay between requests |

## Adding Test Tasks

Use the `add_task()` method to define endpoints to test:

```python
# Simple GET request
perf.add_task(endpoint="/health", method="GET")

# GET with parameters
perf.add_task(
    endpoint="/users",
    method="GET",
    params={"page": 1}
)

# POST request
perf.add_task(
    endpoint="/login",
    method="POST",
    json={"username": "test", "password": "test123"}
)

# PUT request
perf.add_task(
    endpoint="/users/1",
    method="PUT",
    json={"name": "Updated"}
)

# DELETE request
perf.add_task(endpoint="/users/1", method="DELETE")

# With headers
perf.add_task(
    endpoint="/protected",
    method="GET",
    headers={"Authorization": "Bearer token"}
)
```

## Run the Test

```python
results = perf.run()
print(results)
```

## Returned Metrics

The `run()` method returns a dictionary with:

```python
{
    'total_requests': 1500,        # Total requests made
    'successful_requests': 1485,  # Successful requests
    'failed_requests': 15,        # Failed requests
    'success_rate': 99.0,         # Success percentage
    'avg_response_time': 45.2,    # Average time in ms
    'min_response_time': 12.1,    # Minimum time in ms
    'max_response_time': 89.7,    # Maximum time in ms
    'requests_per_second': 150.0, # Requests per second
    'duration': 10,               # Actual duration in seconds
    'users': 10                  # Concurrent users
}
```

## Complete Example: Load Test

```python
from rapidtest import Performance

# Configure load test
perf = Performance(
    base_url="http://localhost:8000",
    users=50,          # 50 concurrent users
    duration=30,       # 30 seconds
    timeout=15,        # 15 seconds timeout
    delay=0.2          # 200ms between requests
)

# Add tasks
print("Setting up load test...")

# Health endpoint test
perf.add_task(endpoint="/health", method="GET")

# User list test
perf.add_task(endpoint="/users", method="GET")

# User creation test
perf.add_task(
    endpoint="/users",
    method="POST",
    json={"name": "Load Test User", "email": "load@test.com"}
)

# Run test
print("\n🚀 Starting load test...\n")
results = perf.run()

# Analyze results
print("\n📊 RESULTS SUMMARY:")
print(f"   Success: {results['success_rate']}%")
print(f"   Throughput: {results['requests_per_second']} req/s")
print(f"   Average time: {results['avg_response_time']}ms")
```

## Example: Result Validation

```python
from rapidtest import Performance

def run_and_validate():
    perf = Performance(
        base_url="http://localhost:8000",
        users=100,
        duration=60,
        timeout=10
    )
    
    perf.add_task(endpoint="/api/health", method="GET")
    results = perf.run()
    
    # Validations
    assert results['success_rate'] >= 95, f"Success rate too low: {results['success_rate']}%"
    assert results['avg_response_time'] <= 500, f"Average time too high: {results['avg_response_time']}ms"
    assert results['requests_per_second'] >= 10, f"Throughput too low: {results['requests_per_second']}"
    
    print(f"✅ All validations passed!")
    return results

run_and_validate()
```

## Example: Multiple Scenarios

```python
from rapidtest import Performance

def test_api_endpoints():
    scenarios = [
        {
            "name": "Health Check",
            "endpoint": "/health",
            "method": "GET",
            "expected_success_rate": 99,
            "max_response_time": 200
        },
        {
            "name": "User List",
            "endpoint": "/users",
            "method": "GET",
            "expected_success_rate": 95,
            "max_response_time": 500
        },
        {
            "name": "User Creation",
            "endpoint": "/users",
            "method": "POST",
            "json": {"name": "Test", "email": "test@example.com"},
            "expected_success_rate": 90,
            "max_response_time": 1000
        }
    ]
    
    for scenario in scenarios:
        print(f"\n🧪 Testing: {scenario['name']}")
        
        perf = Performance(
            base_url="http://localhost:8000",
            users=20,
            duration=10
        )
        
        perf.add_task(
            endpoint=scenario["endpoint"],
            method=scenario["method"],
            json=scenario.get("json")
        )
        
        results = perf.run()
        
        # Validate against expectations
        if results['success_rate'] < scenario['expected_success_rate']:
            print(f"   ⚠️  Warning: success rate {results['success_rate']}% < {scenario['expected_success_rate']}%")
        
        if results['avg_response_time'] > scenario['max_response_time']:
            print(f"   ⚠️  Warning: time {results['avg_response_time']}ms > {scenario['max_response_time']}ms")

test_api_endpoints()
```

## Results Interpretation

| Indicator | Ideal Value | Meaning |
|-----------|-------------|---------|
| `success_rate` | ≥ 95% | API is stable |
| `avg_response_time` | ≤ 500ms | Good response times |
| `requests_per_second` | High | Higher throughput |
| `max_response_time` | ≤ 2x average | No significant outliers |

## Tips for Effective Testing

1. **Start gradually**: Begin with few users and increase
2. **Measure baseline**: First establish a baseline
3. **Isolate endpoints**: Test one endpoint at a time for clear results
4. **Consider delay**: Very low delay can saturate the server
5. **Monitor the server**: Watch CPU, memory, and API connections

## Next Step

Mastered the basics? Explore more in:
- [API Reference](../api/performance.md)