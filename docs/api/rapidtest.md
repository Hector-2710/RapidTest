# RapidTest API Reference

## Test Class

The main class for performing REST API integration tests.

```python
from rapidtest import Test
```

### Constructor

```python
Test(
    *, 
    url: str | None = None, 
    app: Any | None = None, 
    asgi_mode: bool = False, 
    global_headers: dict[str, str] | None = None
)
```

**Parameters:**
- `url` (str | None): The base URL of the API (e.g., 'http://localhost:8000'). Required when `asgi_mode=False`.
- `app` (Any | None): ASGI app instance. Required when `asgi_mode=True`.
- `asgi_mode` (bool): Enable ASGI direct testing mode. Default is `False`.
- `global_headers` (dict[str, str] | None): Global headers to be applied to all requests (optional).

**Example:**
```python
# HTTP mode
tester = Test(url="http://localhost:8000")

# ASGI mode
from myapp.asgi import application
tester = Test(app=application, asgi_mode=True)
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

### Global Headers Management

```python
tester.set_global_headers({"x-api-key": "secret-key"})
tester.clear_global_headers()
```