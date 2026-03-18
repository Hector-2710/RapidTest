# Examples

This page contains practical examples demonstrating RapidTest in various scenarios.

## Basic API Testing

### Simple Health Check

```python
from rapidtest import Test

# Test API health endpoint
api = Test(url="http://localhost:8000")
api.get(path="/health", status=200)
```

### ASGI Health Check (Faster testing)

No server required, tests run directly against the app instance.

```python
from myapp.main import app
from rapidtest import Test

api = Test(app=app, asgi_mode=True)
api.get(path="/health", status=200)
```

### CRUD Operations

```python
from rapidtest import Test

api = Test(url="http://localhost:8000")

# Create
user_data = {"name": "John Doe", "email": "john@example.com"}
response = api.post(path="/users", json=user_data, status=201)
user_id = response.json()["id"]

# Read
api.get(path=f"/users/{user_id}", status=200)

# Update
api.patch(path=f"/users/{user_id}", json={"name": "Jane Doe"}, status=200)

# Delete
api.delete(path=f"/users/{user_id}", status=204)
```

## Using Fake Data

```python
from rapidtest import Test, data

api = Test(url="http://localhost:8000")

# Generate realistic test data
fake_user = {
    "name": data.generate_name(),
    "email": data.generate_email(),
    "phone": data.generate_phone(),
    "address": data.generate_address()
}

api.post(path="/users", json=fake_user, status=201)
```

## Authentication Testing

```python
from rapidtest import Test, data

api = Test(url="http://localhost:8000")

# Generate auth credentials
credentials = data.generate_auth_user()

# Register
api.post(path="/register", json=credentials, status=201)

# Login
login_response = api.post(
    path="/login", 
    json=credentials, 
    status=200
)

# Use token for authenticated requests
token = login_response.json()["token"]
api.get(
    path="/profile",
    headers={"Authorization": f"Bearer {token}"},
    status=200
)
```

## Performance Testing

```python
from rapidtest import Performance

# Load test an endpoint
perf = Performance(
    base_url="http://localhost:8000",
    users=100,        # 100 concurrent users
    duration=60,      # for 60 seconds
    timeout=30        # 30 second timeout
)

perf.add_get_task(path="/api/products")
results = perf.run()

print(f"Success Rate: {results['success_rate']}%")
print(f"Avg Response Time: {results['avg_response_time']}ms")
```

## Error Testing

```python
from rapidtest import Test

api = Test(url="http://localhost:8000")

# Test 404 errors
api.get(path="/users/99999", status=404)

# Test validation errors
api.post(
    path="/users",
    json={"email": "invalid-email"},
    status=400
)

# Test unauthorized access
api.get(path="/admin/users", status=401)
```

## Real-World E-commerce API

```python
from rapidtest import Test, data, Performance

class EcommerceAPITest:
    def __init__(self, base_url):
        self.api = Test(url=base_url)
        
    def test_product_catalog(self):
        """Test product listing and details."""
        # List products
        products = self.api.get(
            path="/products",
            params={"category": "electronics", "limit": 10},
            status=200
        )
        
        # Get specific product
        product_id = products.json()["data"][0]["id"]
        self.api.get(
            path=f"/products/{product_id}",
            status=200
        )
    
    def test_shopping_cart(self):
        """Test cart operations."""
        # Add item to cart
        cart_item = {
            "product_id": 123,
            "quantity": 2,
            "size": "M",
            "color": "blue"
        }
        
        self.api.post(
            path="/cart/items",
            json=cart_item,
            status=201
        )
        
        # View cart
        cart = self.api.get(path="/cart", status=200)
        
        # Update quantity
        self.api.patch(
            path="/cart/items/123",
            json={"quantity": 3},
            status=200
        )
        
        # Remove item
        self.api.delete(
            path="/cart/items/123",
            status=204
        )
    
    def test_checkout_process(self):
        """Test complete checkout flow."""
        # Create order
        order_data = {
            "items": [{"product_id": 123, "quantity": 1}],
            "shipping_address": data.generate_address(),
            "payment_method": "credit_card"
        }
        
        order = self.api.post(
            path="/orders",
            json=order_data,
            status=201
        )
        
        order_id = order.json()["order_id"]
        
        # Process payment
        payment_data = {
            "order_id": order_id,
            "amount": 99.99,
            "currency": "USD"
        }
        
        self.api.post(
            path="/payments",
            json=payment_data,
            status=200
        )
        
        # Check order status
        self.api.get(
            path=f"/orders/{order_id}",
            status=200
        )

# Usage
ecommerce_test = EcommerceAPITest("https://api.shop.example.com")
ecommerce_test.test_product_catalog()
ecommerce_test.test_shopping_cart()
ecommerce_test.test_checkout_process()
```

## CI/CD Integration

```python
#!/usr/bin/env python3
"""
API Tests for CI/CD Pipeline
Run with: python api_tests.py
Exit code 0 = all tests passed
Exit code 1 = at least one test failed
"""

import sys
from rapidtest import Test, data

def run_smoke_tests():
    """Essential tests that must pass before deployment."""
    api = Test(url="https://staging.example.com")
    
    try:
        # Health check
        api.get(path="/health", status=200)
        
        # Database connectivity
        api.get(path="/db-status", status=200)
        
        # Authentication service
        auth_user = data.generate_auth_user()
        api.post(path="/auth/validate", json=auth_user, status=200)
        
        print("✅ All smoke tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Smoke test failed: {e}")
        return False

def run_regression_tests():
    """Extended tests for full validation."""
    api = Test(url="https://staging.example.com")
    
    test_cases = [
        ("User Registration", "/users", {"username": data.generate_name()}),
        ("Product Creation", "/products", {"name": "Test Product", "price": 99.99}),
        ("Order Processing", "/orders", {"product_id": 1, "quantity": 2}),
    ]
    
    failed_tests = []
    
    for test_name, endpoint, data in test_cases:
        try:
            api.post(path=endpoint, json=data, status=201)
            print(f"✅ {test_name} - PASSED")
        except Exception as e:
            print(f"❌ {test_name} - FAILED: {e}")
            failed_tests.append(test_name)
    
    return len(failed_tests) == 0

if __name__ == "__main__":
    print("🚀 Running API tests...")
    
    # Run smoke tests first
    if not run_smoke_tests():
        sys.exit(1)
    
    # Run full regression suite
    if not run_regression_tests():
        sys.exit(1)
    
    print("🎉 All tests passed!")
    sys.exit(0)
```

## Microservices Testing

```python
from rapidtest import Test

# Test multiple microservices
services = {
    "user-service": "http://user-service:8001",
    "order-service": "http://order-service:8002", 
    "payment-service": "http://payment-service:8003",
}

for service_name, service_url in services.items():
    print(f"Testing {service_name}...")
    
    api = Test(url=service_url)
    
    # Health check for each service
    api.get(path="/health", status=200)
    
    # Service-specific tests
    if service_name == "user-service":
        api.get(path="/users", status=200)
    elif service_name == "order-service":
        api.get(path="/orders", status=200)
    elif service_name == "payment-service":
        api.get(path="/payment-methods", status=200)

print("✅ All microservices are healthy")
```

These examples show how RapidTest can be integrated into various testing scenarios from simple API validation to complex CI/CD pipelines.