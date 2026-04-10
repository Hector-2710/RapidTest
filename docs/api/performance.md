# Performance Testing API

Simple performance testing module using requests and threading for basic load testing.

```python
from rapidtest import Performance
```

## Performance Class

### Constructor

```python
Performance(
    *,
    base_url: str | None = None,
    users: int = 10,
    duration: int = 10,
    timeout: int = 10,
    delay: float = 0.1
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `base_url` | str | None | Base URL to test (required for run) |
| `users` | int | 10 | Number of concurrent users to simulate |
| `duration` | int | 10 | Test duration in seconds |
| `timeout` | int | 10 | Max request timeout in seconds |
| `delay` | float | 0.1 | Delay between requests in seconds |

**Example:**
```python
perf_test = Performance(
    base_url="http://localhost:8000",
    users=50,
    duration=30,
    timeout=5,
    delay=0.1
)
```

### Methods

#### add_task

```python
add_task(
    *,
    endpoint: str,
    method: str = "GET",
    params: dict | None = None,
    headers: dict | None = None,
    json: dict | None = None,
    data: dict | str | None = None
)
```

Add a request task to be tested.

**Parameters:**
- `endpoint` (str): URL endpoint to test (e.g., '/api/users')
- `method` (str): HTTP method (GET, POST, PUT, PATCH, DELETE). Default is "GET".
- `params` (dict | None): Query parameters
- `headers` (dict | None): HTTP headers
- `json` (dict | None): JSON body for POST/PUT/PATCH
- `data` (dict | str | None): Form data for POST

**Example:**
```python
# GET request
perf_test.add_task(endpoint="/api/users")

# GET with params
perf_test.add_task(endpoint="/api/users", params={"page": 1})

# POST with JSON
perf_test.add_task(
    endpoint="/api/users",
    method="POST",
    json={"name": "John", "email": "john@example.com"}
)

# POST with form data
perf_test.add_task(
    endpoint="/login",
    method="POST",
    data={"username": "john", "password": "secret"}
)

# DELETE request
perf_test.add_task(endpoint="/api/users/1", method="DELETE")
```

#### run

```python
run() -> Dict[str, Any]
```

Execute the performance test and return detailed statistics.

**Returns:**
A dictionary containing test results:

```python
{
    'total_requests': 1500,
    'successful_requests': 1485,
    'failed_requests': 15,
    'success_rate': 99.0,
    'avg_response_time': 45.2,
    'min_response_time': 12.1,
    'max_response_time': 89.7,
    'requests_per_second': 150.0,
    'duration': 10,
    'users': 50
}
```

**Result Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `total_requests` | int | Total number of requests made |
| `successful_requests` | int | Number of successful requests (status 200-399) |
| `failed_requests` | int | Number of failed requests |
| `success_rate` | float | Success percentage (0-100) |
| `avg_response_time` | float | Average response time in milliseconds |
| `min_response_time` | float | Minimum response time in milliseconds |
| `max_response_time` | float | Maximum response time in milliseconds |
| `requests_per_second` | float | Throughput (requests per second) |
| `duration` | int | Test duration in seconds |
| `users` | int | Number of concurrent users |

## Complete Example

```python
from rapidtest import Performance

# Initialize performance test
perf_test = Performance(
    base_url="http://localhost:8000",
    users=100,  # 100 concurrent users
    duration=60,  # Test for 60 seconds
    timeout=10  # 10 second timeout
)

# Add multiple endpoints to test
perf_test.add_task(endpoint="/api/health", method="GET")
perf_test.add_task(endpoint="/api/users", method="GET")
perf_test.add_task(
    endpoint="/api/users",
    method="POST",
    json={"name": "Test", "email": "test@example.com"}
)

# Run test and get results
results = perf_test.run()

# Access specific metrics
print(f"Success Rate: {results['success_rate']}%")
print(f"Average Response Time: {results['avg_response_time']}ms")
print(f"Requests per Second: {results['requests_per_second']}")
```

## Console Output

The performance test provides real-time console output showing:

- 🚀 Test configuration (URL, users, duration)
- 📋 Tasks defined
- 📊 Detailed results table with all metrics
- 🟢 Performance indicators (excellent/good/poor)

## Thread Safety

The Performance class uses threading locks to ensure thread-safe collection of results from multiple concurrent workers.

## Error Handling

- **Network Errors**: Captured and counted as failed requests
- **Timeouts**: Automatically handled with configurable timeout values
- **Invalid Responses**: Non-2xx/3xx status codes counted as failures