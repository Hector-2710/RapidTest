# 🚀 Quick Start

Get up and running with RapidTest in just a few minutes! ⚡

## 1. 🔧 Initialize RapidTest

### ⚡ ASGI mode with the same class

```python
from rapidtest import ASGITest
from backend.main import app

tester = ASGITest(app=app)
tester.get(path="/health", status=200)
```

### 📋 Response Body Validation

```python
tester.get(
    path="/", 
    status=200,
    expected_json= "API running"
)
```

> **💡 NOTE:** 
Remember that the expected_json will depend solely on how the endpoint is defined.

## 4. 🚨 Error Handling

RapidTest provides clear, colorized output when tests fail:

- ✅ Green for successful tests
- ❌ Red for failed tests  
- 📊 Detailed error information

## 🎯 What's Next?

- ⚡ Learn about [HTTP Methods](../learn/http-methods.md)
- 📚 Check out our [API Reference](../api/rapidtest.md)