# Agent Instructions for RapidTest

This document provides guidelines for agents working on the RapidTest codebase.

## Project Overview

RapidTest is a lightweight Python library for REST API testing with functional checks, ASGI direct mode, fake data generation, and basic performance testing.

## Build/Lint/Test Commands

### Running Tests

```bash
# Run all tests
python tests.py

# Run with pytest (if test files exist)
pytest

# Run a single test function
pytest -k "test_name"

# Run a specific test file
pytest path/to/test_file.py

# Run tests with verbose output
pytest -v

# Run tests with coverage
pytest --cov=rapidtest --cov-report=term-missing
```

### Installation

```bash
# Create virtual environment
python -m venv venv

# Activate venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install all dependencies
pip install -r requirements.txt

# Install rapidtest in development mode
pip install -e .
```

### Code Quality

```bash
# Format code (if black/ruff configured)
black .

# Lint code (if ruff configured)
ruff check .

# Type checking (if mypy configured)
mypy rapidtest/
```

### CLI Commands

```bash
# Generate test skeleton
rapidtest skeleton -o my_test.py

# With custom name
rapidtest skeleton -n "My API" -o test.py

# Overwrite existing
rapidtest skeleton -o test.py --force
```

## Code Style Guidelines

### Python Version
- Target Python 3.7+ compatibility (as per pyproject.toml)
- Use modern type hints where possible

### Import Conventions

1. **Standard library imports first**
2. **Third-party imports second**
3. **Local application imports third**
4. **Separate each group with a blank line**

```python
# Standard library
import json
import time
from typing import Any, Annotated

# Third-party
import requests
from faker import Faker

# Local (relative imports)
from rapidtest.Utils import show_connection_error
from .ASGITest import ASGITest
```

### Type Hints

- Use `Annotated` for parameter documentation in public APIs
- Use modern union syntax (`X | None`) over `Optional[X]`
- Use lowercase type aliases (e.g., `type Response = ...`)
- Mark private types with leading underscore when appropriate

```python
# Good
from typing import Annotated

def get(
    self,
    path: Annotated[str | None, "The API endpoint to call"] = None,
    status: Annotated[int, "Expected HTTP status code"] = 200,
) -> Response:
    ...

# Good - modern union syntax
def _merge_headers(self, headers: dict[str, str] | None) -> dict[str, str] | None:
    ...

# Good - type aliases
type Response = requests.Response | None
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Classes | PascalCase | `Test`, `ASGIResponse`, `StatusCode` |
| Methods/Functions | snake_case | `get()`, `_merge_headers()`, `generate_email()` |
| Variables | snake_case | `response_json`, `status_code`, `global_headers` |
| Constants | UPPER_SNAKE | `MAX_TIMEOUT`, `DEFAULT_STATUS` |
| Modules | snake_case | `utils.py`, `asgi_test.py` |
| Type aliases | PascalCase | `Response` |

### Class Structure

- Use docstrings for all public classes and methods
- Private methods should be prefixed with `_`
- Use `@staticmethod` for utility methods that don't need `self`

```python
class Test:
    """
    Main class for REST API integration tests.
    
    This class allows making HTTP requests and ASGI requests, validating
    responses, and printing detailed test reports to the console.
    """
    
    def __init__(self, *, url: str | None = None, asgi_mode: bool = False):
        """Initializes the test client."""
        self.url = url
    
    def get(self, *, path: str | None = None, status: int = 200) -> Response:
        """Performs a GET request and validates status code and response body."""
        ...
    
    def _internal_method(self):
        """Private helper method."""
        ...
```

### Error Handling

- Use specific exception types when possible
- Catch exceptions at appropriate levels
- Provide informative error messages

```python
# Good - specific exception with clear message
if self.asgi_mode:
    if app is None:
        raise AttributeError("'app' is required when asgi_mode=True")
elif not self.url:
    raise AttributeError("'url' is required when asgi_mode=False")

# Good - try/except with context
try:
    response = method_func(url, **request_kwargs)
except Exception as e:
    show_connection_error(url, e)
    return None
```

### Function Parameters

- Use keyword-only arguments (after `*`) for most function parameters
- Provide sensible defaults where appropriate
- Document parameter meanings with Annotated types

```python
def post(
    self,
    *,
    path: Annotated[str | None, "The API endpoint to call"] = None,
    status: Annotated[int, "Expected HTTP status code"] = 201,
    json: Annotated[dict[str, Any] | None, "JSON data to send"] = None,
    headers: Annotated[dict[str, str] | None, "HTTP headers"] = None,
    **kwargs,
) -> Response:
    ...
```

### Enum Usage

- Use `enum.IntEnum` for HTTP status codes
- Name enum members descriptively with numeric suffix

```python
import enum

class StatusCode(enum.IntEnum):
    OK_200 = 200
    CREATED_201 = 201
    NOT_FOUND_404 = 404
    INTERNAL_SERVER_ERROR_500 = 500
```

### File Organization

**rapidtest package structure:**
```
rapidtest/
├── __init__.py      # Public API exports
├── Test.py          # Main Test class
├── ASGITest.py      # ASGI testing support
├── AGSIResponse.py  # ASGI response wrapper
├── Performance.py   # Performance testing
├── StatusCode.py    # HTTP status code enum
├── data.py          # Fake data generation
├── Utils.py         # Utility functions
└── types.py         # Type aliases

# CLI (project root)
rapidtest_cli.py     # CLI entry point
```

### Async/Await

- Use `async def` for async endpoints (FastAPI)
- Use `asyncio.run()` for top-level async calls
- Mark async helper methods appropriately

```python
async def get_user(user_id: uuid.UUID, db: GetSession):
    ...

async def _make_asgi_request(self, method: str | None, path: str | None, ...):
    ...
```

### Docstring Format

Use Google-style docstrings:

```python
def generate_email() -> str:
    """Generates a random email address.
    
    Args:
        None
    
    Returns:
        A random email address as a string.
    """
    return fake.email()
```

## Working with this Codebase

### Adding New HTTP Methods

1. Add the method to `Test` class in `Test.py`
2. Add corresponding method to `ASGITest` class in `ASGITest.py`
3. Export from `__init__.py`
4. Update docstrings and type hints

### Adding Data Generators

1. Add method to `data.py` class
2. Use Faker library for realistic data
3. Document with docstring
4. Export from `__init__.py`

### Modifying Status Codes

1. Edit `StatusCode` enum in `StatusCode.py`
2. Follow naming pattern: `NAME_NUMBER`
3. Use IntEnum for integer comparison

## Testing Backend Changes

The backend (FastAPI app) uses the test framework internally:

```python
# tests.py demonstrates testing the backend
from rapidtest.Test import Test
from rapidtest.data import data
from rapidtest.StatusCode import StatusCode
from backend.main import app

test = Test(app=app, asgi_mode=True)

# Run individual test
test.post(
    path="/token",
    status=StatusCode.OK_200,
    data={"username": "caja", "password": "caja"}
)
```
