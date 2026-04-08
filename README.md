![RapidTest Logo](docs/images/RapidTest-logo.png)

# RapidTest

A lightweight library for REST API testing with ASGI/HTTP mode, fake data generation, and performance testing.

## Features

- **ASGI Testing** - Test FastAPI/Starlette apps directly without HTTP server
- **HTTP Testing** - Test external APIs with `GET`, `POST`, `PUT`, `PATCH`, `DELETE`
- Built-in response validation (status, JSON body, required keys)
- Fake data generation with Faker
- Performance testing with concurrent users (`threading` + `requests`)
- Test any endpoint with just one line of code

## Installation

```bash
pip install rapidtest
```

## CLI

Generate a test skeleton file:

```bash
rapidtest init
```
## Quick Start (ASGI mode)

Use this when you want to test your ASGI app directly (for example FastAPI) without network overhead.

```python
from backend.main import app
from rapidtest import ASGITest, StatusCode


tester = ASGITest(app=app)

tester.get(
    path="/ping",
    status=StatusCode.OK_200,
    json={"ok": True}
)
```

**Output:**
```
✅ 1. PASSED
time: 0.01 s
```

## Quick Start (HTTP mode)

```python
from rapidtest import HTTPTest, StatusCode

api = HTTPTest(url="http://localhost:8000")

api.get(
    path="/health",
    status=StatusCode.OK_200,
    keys=["message"]
)

payload = {"username": "hector", "password": "secret"}
api.post(
    path="/login",
    json=payload,
    status=StatusCode.OK_200,
    keys=["token"]
)
```

**Output:**
```
✅ 1. PASSED
✅ 2. PASSED
time: 0.05 s
```

## Data Generation

```python
from rapidtest import Data

auth = Data.generate_auth_user()

print(auth)  # {"username": "...", "password": "..."}
```

Useful helpers include:

- `generate_name()`
- `generate_email()`
- And more...

## Performance Testing

```python
from rapidtest import Performance

perf = Performance(
    base_url="http://localhost:8000",
    users=20,
    duration=15,
    timeout=10
)

# Add multiple endpoints with different methods
perf.add_task(endpoint="/health", method="GET")
perf.add_task(endpoint="/login", method="POST", json={"user": "test"})

results = perf.run()
```

Returned metrics:

- `total_requests`
- `successful_requests`
- `failed_requests`
- `success_rate`
- `avg_response_time`
- `min_response_time`
- `max_response_time`
- `requests_per_second`
- `duration`
- `users`

## Requirements

- Python `>=3.7`
- `requests>=2.25.1`
- `faker>=13.0.0`

## Project Info

- Version: `0.6.0`
- Author: Hector Rosales
- License: MIT
- Homepage: https://github.com/hector-2710/rapidtest
- Issues: https://github.com/hector-2710/rapidtest/issues