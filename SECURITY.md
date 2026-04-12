# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability in RapidTest, please report it responsibly.

### How to Report

1. **DO NOT** create a public GitHub Issue for security vulnerabilities
2. Email the maintainer directly: `h.rosales01@ufromail.cl`
3. Include in your report:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Any possible mitigations

### What to Expect

- Acknowledgment of your report within **48 hours**
- Regular updates on the progress of fixing the vulnerability
- Credit in the release notes (if desired)

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.6.x   | ✅ Yes             |
| 0.5.x   | ✅ Yes             |
| 0.4.x   | ⚠️ Security fixes |
| < 0.4   | ❌ No              |

## Security Best Practices

When using RapidTest:

### 1. Don't commit secrets
```python
# ❌ BAD
api = HTTPTest(url="http://api.example.com", headers={"Authorization": "secret-key"})

# ✅ GOOD - Use environment variables
import os
api = HTTPTest(url=os.getenv("API_URL"), headers={"Authorization": os.getenv("API_KEY")})
```

### 2. Use timeouts
```python
# ✅ GOOD - Always set reasonable timeouts
api = HTTPTest(url="http://localhost:8000", timeout=10)
```

### 3. Validate responses
```python
# ✅ GOOD - Verify response content
api.get(path="/secure-data", status=200, expected_json={"data": "expected"})
```

## Security Audits

We welcome security audits and will credit responsible disclosures.

---

Thank you for helping keep RapidTest secure! 🔒