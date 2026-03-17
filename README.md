![RapidTest Logo](docs/images/RapidTest-logo.png)

# RapidTest

A lightweight library for REST API testing with functional checks, ASGI direct mode, fake data generation, and basic performance testing.

## Features

- Simple HTTP testing with `GET`, `POST`, `PUT`, `PATCH`, `DELETE`
- Built-in response validation (status, JSON body, required keys)
- ASGI direct mode for testing app instances without running an HTTP server
- Fake data generation with Faker
- Basic load testing with concurrent users (`threading` + `requests`)
- Test any endpoint with just one line of code

## Installation

```bash
pip install rapidtest
```

## Quick Start (HTTP mode)

```python
from rapidtest import Test, StatusCode

api = Test(url="http://localhost:8000")

# GET with status + key validation
api.get(
    path="/health",
    status=StatusCode.OK_200,
    keys=["message"]
)

# POST with request body + expected response body
payload = {"username": "hector", "password": "secret"}
api.post(
    path="/login",
    json=payload,
    status=StatusCode.OK_200,
    keys=["token"]
)
```

## Quick Start (ASGI mode)

Use this when you want to test your ASGI app directly (for example FastAPI) without network overhead.

```python
from fastapi import FastAPI
from rapidtest import Test, StatusCode

app = FastAPI()

@app.get("/ping")
def ping():
    return {"ok": True}

tester = Test(app=app, asgi_mode=True)

tester.get(
    path="/ping",
    status=StatusCode.OK_200,
    json={"ok": True}
)
```


## Data Generation

```python
from rapidtest import data

auth = data.generate_auth_user()

print(auth)  # {"username": "...", "password": "..."}
```

Useful helpers include:

- `generate_name()`
- `generate_email()`
- `generate_phone()`
- `more..`

## Performance Testing

```python
from rapidtest import Performance

perf = Performance(
    base_url="http://localhost:8000",
    users=20,
    duration=15,
    timeout=10
)

perf.add_get_task(endpoint="/health")
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

- Version: `0.4.0`
- Author: Hector Rosales
- License: MIT
- Homepage: https://github.com/hector-dev/rapidtest
- Issues: https://github.com/hector-dev/rapidtest/issues
