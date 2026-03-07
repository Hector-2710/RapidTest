# 🌐 HTTP Methods with RapidTest

Introduction to HTTP methods, learn when and how to use each one effectively in your API. ⚡

## 📖 Overview

HTTP methods define the type of operation you want to perform on a resource. RapidTest supports all major HTTP methods with automatic validation.

## 1. 📥 GET Method

### 🎯 Purpose
 - Retrieve data from the server.

### 💡 When to Use
 - Getting and reading information

## 2. 📤 POST Method

### 🎯 Purpose
 - Create new resources on the server.

### 💡 When to Use
- Creating new users
- Submitting forms
- Authentication requests

## 3. 🔄 PUT Method

### 🎯 Purpose
Replace entire resources.

### 💡 When to Use
- Updating complete user profiles
- Full resource updates


## 4. 🎨 PATCH Method

### 🎯 Purpose
Partially update existing resources.

### 💡 When to Use
- Updating specific fields
- Partial data modifications


## 5. 🗑️ DELETE Method

### 🎯 Purpose
Remove resources from the server.

### 💡 When to Use
- Deleting user accounts
- Removing items


## 🔗  Example of API with FastAPI

Here's a basic guide on how to use HTTP methods with FastAPI: 🚀

### 🔧 Basic FastAPI 

```python
# main.py - Simple FastAPI server
from fastapi import FastAPI

app = FastAPI()

# Simple in-memory storage
users = {}
counter = 1

# 📥 GET endpoints
@app.get("/")
def health_check():
    return {"message": "API is working!"}

# 📤 POST endpoint
@app.post("/users")
def create_user(user_data: dict):
    global counter
    user_data["id"] = counter
    users[counter] = user_data
    counter += 1
    return user_data

# 🔄 PUT endpoint
@app.put("/users/{user_id}")
def update_user(user_id: int, user_data: dict):
    if user_id in users:
        user_data["id"] = user_id
        users[user_id] = user_data
        return user_data
    return {"error": "User not found"}, 404

# 🎨 PATCH endpoint
@app.patch("/users/{user_id}")
def patch_user(user_id: int, updates: dict):
    if user_id in users:
        users[user_id].update(updates)
        return users[user_id]
    return {"error": "User not found"}, 404

# 🗑️ DELETE endpoint
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id in users:
        del users[user_id]
        return {"message": "User deleted"}
    return {"error": "User not found"}, 404

```

### 🏃‍♂️ Quick Setup

1. **Install FastAPI:**
```bash
pip install "fastapi[standard]"
```

2. **Run server:**
```bash
fastapi dev     
```

## 🎯 What's Next?

- 🚀 Learn about [HTTP Headers](../learn/http-headers.md)
- 📚 Read the [API Reference](../api/rapidtest.md)