# 📋 HTTP Headers with RapidTest

Introduction to HTTP headers, learn when and how to use the most important ones in your API. ⚡

## 📖 Overview

HTTP headers provide essential metadata about requests and responses, headers exist for authentication, content negotiation, and more.

## 1. 🔐 Authorization Header

### 🎯 Purpose
 - Authenticate and authorize API requests.

### 💡 When to Use
 - Protected endpoints
 - User authentication

### 📝 Examples

#### Bearer Token
```python
from rapidtest import RapidTest

# Test with Bearer token
test = RapidTest()
response = test.get(
    "/protected-endpoint",
    headers={"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOi..."}
)
```

## 2. 📄 Content-Type Header

### 🎯 Purpose
 - Specify the format of request/response body.

### 💡 When to Use
- Sending JSON data
- Form submissions
- File uploads

### 📝 Examples

#### JSON Data
```python
# Sending JSON data
data = {"name": "John", "email": "john@example.com"}
response = test.post(
    "/users",
    json=data,  # RapidTest automatically sets Content-Type: application/json
    headers={"Accept": "application/json"}
)
```
## 3. 🍪 Cookie Headers

### 🎯 Purpose
 - Manage session state and user preferences.

### 💡 When to Use
- Session management
- User preferences
- Authentication tokens

### 📝 Examples

#### Sending Cookies
```python
# Test with session cookie
response = test.get(
    "/dashboard",
    headers={
        "Cookie": "session_id=abc123; user_pref=dark_mode"
    }
)
```

### 🧪 Testing Headers with RapidTest

RapidTest makes testing HTTP headers incredibly simple with its intuitive syntax. You can easily verify both request headers and response headers. ✨


## 🎯 What's Next?

- 🚀 Check the [Learn About Threads](../learn/threads.md)
- 📚 Read the [Watch The Tutorials](../tutorial/basic.md)