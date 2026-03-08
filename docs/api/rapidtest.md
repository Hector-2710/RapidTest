# RapidTest API Reference

## Test Class

The main class for performing REST API integration tests.

```python
from rapidtest import Test
```

### Constructor

```python
Test(*, url: str)
```

**Parameters:**
- `url` (str): The base URL of the API (e.g., 'http://localhost:8000')

**Example:**
```python
tester = Test(url="http://localhost:8000")
```

### HTTP Methods

All HTTP methods share the following common parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `endpoint` | str | Required | Endpoint path (e.g., '/users') |
| `expected_status` | int | 200 | Expected HTTP status code |
| `expected_body` | dict | None | Expected JSON body in response |
| `json` | dict/list/str/int/float/bool | None | JSON data to send in request body |
| `data` | str/bytes/dict | None | Request body data |
| `params` | dict | None | Query parameters for the URL |
| `headers` | dict | None | Additional HTTP headers |

#### GET Request

```python
tester.get(
    endpoint="/users",
    expected_status=200,
    headers={"Authorization": "Bearer token"},
    params={"page": 1}
)
```

#### POST Request

```python
user_data = {"username": "john", "email": "john@example.com"}
tester.post(
    endpoint="/users",
    json=user_data,
    expected_status=201,
    expected_body=user_data
)
```

#### PUT Request

```python
tester.put(
    endpoint="/users/1",
    json={"name": "Updated Name"},
    expected_status=200
)
```

#### PATCH Request

```python
tester.patch(
    endpoint="/users/1",
    json={"email": "newemail@example.com"},
    expected_status=200
)
```

#### DELETE Request

```python
tester.delete(
    endpoint="/users/1",
    expected_status=204
)
```

### Response Validation

RapidTest automatically validates:

1. **Status Code**: Compares actual vs expected status code
2. **Response Body**: Compares actual JSON response vs expected body (if provided)

### Error Handling

- **Connection Errors**: Displays clear error messages for network issues
- **Status Code Mismatches**: Shows expected vs actual status codes
- **Body Mismatches**: Highlights differences in response bodies
- **JSON Parsing Errors**: Gracefully handles non-JSON responses

### Return Values

All HTTP methods return a `requests.Response` object on success, or `None` if a critical connection error occurred.

You can access:
- `response.status_code`: HTTP status code
- `response.json()`: JSON response body
- `response.text`: Raw response text  
- `response.headers`: Response headers