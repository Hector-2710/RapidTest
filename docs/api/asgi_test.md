# ASGITest API Reference

Class for performing REST API integration tests directly against ASGI applications without running an HTTP server.

```python
from rapidtest import ASGITest
```

## Constructor

```python
ASGITest(
    app: Any
)
```

**Parameters:**
- `app` (Any): An ASGI application instance (e.g., FastAPI app, Starlette app). Required.

**Example:**
```python
from myapp import app

api = ASGITest(app=app)
```

## HTTP Methods

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

### GET Request

```python
api.get(
    path="/users",
    status=200,
    headers={"Authorization": "Bearer token"},
    params={"page": 1}
)
```

### POST Request

```python
user_data = {"username": "john", "email": "john@example.com"}
api.post(
    path="/users",
    json=user_data,
    status=201,
    expected_json=user_data
)
```

### PUT Request

```python
api.put(
    path="/users/1",
    json={"name": "Updated Name"},
    status=200
)
```

### PATCH Request

```python
api.patch(
    path="/users/1",
    json={"email": "newemail@example.com"},
    status=200
)
```

### DELETE Request

```python
api.delete(
    path="/users/1",
    status=204
)
```

## Response Validation

ASGITest automatically validates:

1. **Status Code**: Compares actual vs expected status code
2. **Response Body**: Compares actual JSON response vs `expected_json` (if provided)
3. **Response Keys**: Validates the presence of expected keys (if `keys` is provided)

## Error Handling

- **ASGI Errors**: Displays clear error messages for ASGI application issues
- **Status Code Mismatches**: Shows expected vs actual status codes
- **Body Mismatches**: Highlights differences in response bodies
- **JSON Parsing Errors**: Gracefully handles non-JSON responses

## Return Values

All HTTP methods return `None`. The response is validated internally and results are printed to console. To access response data, you would need to modify the class to return the response object.

## Resource Management

### close()

```python
api.close()
```

Closes the event loop used by the ASGITest instance. Call this method after completing all tests to clean up resources.

**Example:**
```python
api = ASGITest(app=app)

# Run tests
api.get(path="/health", status=200)

# Clean up
api.close()
```

## Differences from HTTPTest

| Feature | HTTPTest | ASGITest |
|---------|----------|----------|
| Requires server | Yes | No |
| Uses URL | Yes | No |
| Uses app instance | No | Yes |
| Faster execution | No | Yes |
| Returns Response | Yes | No |