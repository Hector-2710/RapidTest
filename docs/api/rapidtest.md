# RapidTest API Reference

## HTTPTest Class

The main class for performing REST API integration tests over HTTP.

```python
from rapidtest import HTTPTest
```

### Constructor

```python
HTTPTest(
    *, 
    url: str | None = None, 
    timeout: int = 30
)
```

**Parameters:**
- `url` (str | None): The base URL of the API (e.g., 'http://localhost:8000'). Required.
- `timeout` (int): Request timeout in seconds. Default is 30.

**Example:**
```python
# HTTP mode
tester = HTTPTest(url="http://localhost:8000")
```

### HTTP Methods

All HTTP methods share the following common parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `path` | str | Required | The API endpoint to call (e.g., '/users') |
| `status` | int | 200/201/204 | Expected HTTP status code |
| `expected_json` | dict | None | Expected JSON body in response |
| `keys` | list[str] | None | A subset of JSON keys that should be contained in the response |
| `json` | dict/list/str/int/float/bool | None | JSON data to send in request body |
| `data` | str/bytes/dict | None | Request body data |
| `params` | dict | None | Query parameters for the URL |
| `headers` | dict | None | Additional HTTP headers |

#### GET Request

```python
tester.get(
    path="/users",
    status=200,
    headers={"Authorization": "Bearer token"},
    params={"page": 1}
)
```

#### POST Request

```python
user_data = {"username": "john", "email": "john@example.com"}
tester.post(
    path="/users",
    json=user_data,
    status=201,
    expected_json=user_data
)
```

#### PUT Request

```python
tester.put(
    path="/users/1",
    json={"name": "Updated Name"},
    status=200
)
```

#### PATCH Request

```python
tester.patch(
    path="/users/1",
    json={"email": "newemail@example.com"},
    status=200
)
```

#### DELETE Request

```python
tester.delete(
    path="/users/1",
    status=204
)
```

### Response Validation

RapidTest automatically validates:

1. **Status Code**: Compares actual vs expected status code
2. **Response Body**: Compares actual JSON response vs `expected_json` (if provided)
3. **Response Keys**: Validates the presence of expected keys (if `keys` is provided)

### Error Handling

- **Connection Errors**: Displays clear error messages for network issues
- **Status Code Mismatches**: Shows expected vs actual status codes
- **Body Mismatches**: Highlights differences in response bodies
- **JSON Parsing Errors**: Gracefully handles non-JSON responses

### Return Values

All HTTP methods return a `Response` object on success, or `None` if a critical connection error occurred.

You can access properties directly:
- `response.status_code`: HTTP status code
- `response.json()`: JSON response body
- `response.text`: Raw response text  
- `response.headers`: Response headers

---

## ASGITest Class

For testing ASGI applications directly without running an HTTP server.

```python
from rapidtest import ASGITest
```

### Constructor

```python
ASGITest(
    *, 
    app: Any,
    timeout: int = 30
)
```

**Parameters:**
- `app` (Any): ASGI app instance. Required.
- `timeout` (int): Request timeout in seconds. Default is 30.

**Example:**
```python
from myapp.asgi import application
tester = ASGITest(app=application)
```

### HTTP Methods

The ASGITest class has the same HTTP methods as HTTPTest (`get`, `post`, `put`, `patch`, `delete`) with the same parameters.

---

## StatusCode Enum

Pre-defined HTTP status codes for use in tests.

```python
from rapidtest import StatusCode

# Usage
tester.get(path="/health", status=StatusCode.OK)
tester.post(path="/users", json=data, status=StatusCode.CREATED)
tester.delete(path="/users/1", status=StatusCode.NO_CONTENT)
```

**Available values:**
- `StatusCode.OK` = 200
- `StatusCode.CREATED` = 201
- `StatusCode.NO_CONTENT` = 204
- `StatusCode.BAD_REQUEST` = 400
- `StatusCode.UNAUTHORIZED` = 401
- `StatusCode.FORBIDDEN` = 403
- `StatusCode.NOT_FOUND` = 404
- `StatusCode.INTERNAL_SERVER_ERROR` = 500
- `StatusCode.SERVICE_UNAVAILABLE` = 503

And more standard HTTP status codes.