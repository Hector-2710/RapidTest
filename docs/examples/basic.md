# Examples

This page contains practical examples demonstrating RapidTest in various scenarios.

## Basic API Testing

### Simple Health Check

```python
from rapidtest import Test

# Test API health endpoint
api = Test(url="http://localhost:8000")
api.get(endpoint="/health", expected_status=200)
```

### CRUD Operations

```python
from rapidtest import Test

api = Test(url="http://localhost:8000")

# Create
user_data = {"name": "John Doe", "email": "john@example.com"}
response = api.post(endpoint="/users", json=user_data, expected_status=201)
user_id = response.json()["id"]

# Read
api.get(endpoint=f"/users/{user_id}", expected_status=200)

# Update
api.patch(endpoint=f"/users/{user_id}", json={"name": "Jane Doe"}, expected_status=200)

# Delete
api.delete(endpoint=f"/users/{user_id}", expected_status=204)
```

## Using Fake Data

```python
from rapidtest import Test, Data

api = Test(url="http://localhost:8000")

# Generate realistic test data
fake_user = {
    "name": Data.generate_name(),
    "email": Data.generate_email(),
    "phone": Data.generate_phone(),
    "address": Data.generate_address()
}

api.post(endpoint="/users", json=fake_user, expected_status=201)
```

## Authentication Testing

```python
from rapidtest import Test, Data

api = Test(url="http://localhost:8000")

# Generate auth credentials
credentials = Data.generate_auth_user()

# Register
api.post(endpoint="/register", json=credentials, expected_status=201)

# Login
login_response = api.post(
    endpoint="/login", 
    json=credentials, 
    expected_status=200
)

# Use token for authenticated requests
token = login_response.json()["token"]
api.get(
    endpoint="/profile",
    headers={"Authorization": f"Bearer {token}"},
    expected_status=200
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

perf.add_get_task(endpoint="/api/products")
results = perf.run()

print(f"Success Rate: {results['success_rate']}%")
print(f"Avg Response Time: {results['avg_response_time']}ms")
```

## Error Testing

```python
from rapidtest import Test

api = Test(url="http://localhost:8000")

# Test 404 errors
api.get(endpoint="/users/99999", expected_status=404)

# Test validation errors
api.post(
    endpoint="/users",
    json={"email": "invalid-email"},
    expected_status=400
)

# Test unauthorized access
api.get(endpoint="/admin/users", expected_status=401)
```

## Real-World E-commerce API

```python
from rapidtest import Test, Data, Performance

class EcommerceAPITest:
    def __init__(self, base_url):
        self.api = Test(url=base_url)
        
    def test_product_catalog(self):
        """Test product listing and details."""
        # List products
        products = self.api.get(
            endpoint="/products",
            params={"category": "electronics", "limit": 10},
            expected_status=200
        )
        
        # Get specific product
        product_id = products.json()["data"][0]["id"]
        self.api.get(
            endpoint=f"/products/{product_id}",
            expected_status=200
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
            endpoint="/cart/items",
            json=cart_item,
            expected_status=201
        )
        
        # View cart
        cart = self.api.get(endpoint="/cart", expected_status=200)
        
        # Update quantity
        self.api.patch(
            endpoint="/cart/items/123",
            json={"quantity": 3},
            expected_status=200
        )
        
        # Remove item
        self.api.delete(
            endpoint="/cart/items/123",
            expected_status=204
        )
    
    def test_checkout_process(self):
        """Test complete checkout flow."""
        # Create order
        order_data = {
            "items": [{"product_id": 123, "quantity": 1}],
            "shipping_address": Data.generate_address(),
            "payment_method": "credit_card"
        }
        
        order = self.api.post(
            endpoint="/orders",
            json=order_data,
            expected_status=201
        )
        
        order_id = order.json()["order_id"]
        
        # Process payment
        payment_data = {
            "order_id": order_id,
            "amount": 99.99,
            "currency": "USD"
        }
        
        self.api.post(
            endpoint="/payments",
            json=payment_data,
            expected_status=200
        )
        
        # Check order status
        self.api.get(
            endpoint=f"/orders/{order_id}",
            expected_status=200
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
from rapidtest import Test, Data

def run_smoke_tests():
    """Essential tests that must pass before deployment."""
    api = Test(url="https://staging.example.com")
    
    try:
        # Health check
        api.get(endpoint="/health", expected_status=200)
        
        # Database connectivity
        api.get(endpoint="/db-status", expected_status=200)
        
        # Authentication service
        auth_user = Data.generate_auth_user()
        api.post(endpoint="/auth/validate", json=auth_user, expected_status=200)
        
        print("✅ All smoke tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Smoke test failed: {e}")
        return False

def run_regression_tests():
    """Extended tests for full validation."""
    api = Test(url="https://staging.example.com")
    
    test_cases = [
        ("User Registration", "/users", {"username": Data.generate_name()}),
        ("Product Creation", "/products", {"name": "Test Product", "price": 99.99}),
        ("Order Processing", "/orders", {"product_id": 1, "quantity": 2}),
    ]
    
    failed_tests = []
    
    for test_name, endpoint, data in test_cases:
        try:
            api.post(endpoint=endpoint, json=data, expected_status=201)
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
    api.get(endpoint="/health", expected_status=200)
    
    # Service-specific tests
    if service_name == "user-service":
        api.get(endpoint="/users", expected_status=200)
    elif service_name == "order-service":
        api.get(endpoint="/orders", expected_status=200)
    elif service_name == "payment-service":
        api.get(endpoint="/payment-methods", expected_status=200)

print("✅ All microservices are healthy")
```

These examples show how RapidTest can be integrated into various testing scenarios from simple API validation to complex CI/CD pipelines.