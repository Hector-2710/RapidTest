# RapidTest API Reference

**Versión:** 0.9.0  
**Python:** >=3.10

Librería para testing de APIs REST con testing ASGI directo, HTTP real y performance testing.

---

## Índice

1. [ASGITest](#asgitest) - Testing directo ASGI
2. [HTTPTest](#httptest) - Testing via HTTP real
3. [Performance](#performance) - Load testing
4. [Data](#data) - Generación de datos fake
5. [StatusCode](#statuscode) - Códigos HTTP

---

## ASGITest

Testing directo de aplicaciones ASGI (FastAPI, Starlette, etc.) sin necesidad de levantar un servidor HTTP.

```python
from rapidtest import ASGITest

api = ASGITest(app)
```

### Constructor

```python
ASGITest(app)
```

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `app` | ASGI app | Aplicación ASGI (FastAPI, Starlette, etc.) |

### Métodos HTTP

#### `get(path, status=200, expected_json=None, keys=None, params=None, headers=None)`

Realiza una petición GET.

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `path` | str | *requerido* | Ruta del endpoint (ej: `/users/1`) |
| `status` | int | 200 | Código de estado esperado |
| `expected_json` | dict | None | JSON exacto que debe retornar |
| `keys` | list | None | Keys que deben existir en la respuesta |
| `params` | dict | None | Query parameters |
| `headers` | dict | None | Headers HTTP |

**Ejemplo:**
```python
api = ASGITest(app)

# Verificar status code
api.get("/health", status=200)

# Verificar JSON exacto
api.get("/users/1", expected_json={"id": 1, "name": "Alice"})

# Verificar que ciertas keys existen
api.get("/users", keys=["id", "name", "email"])

# Con query parameters
api.get("/users", params={"role": "admin"})

# Con headers
api.get("/profile", headers={"Authorization": "Bearer token"})
```

---

#### `post(path, status=201, json=None, expected_json=None, keys=None, data=None, params=None, headers=None)`

Realiza una petición POST.

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `path` | str | *requerido* | Ruta del endpoint |
| `status` | int | 201 | Código de estado esperado |
| `json` | dict | None | Body JSON |
| `data` | dict | None | Form data (application/x-www-form-urlencoded) |
| `expected_json` | dict | None | JSON exacto que debe retornar |
| `keys` | list | None | Keys que deben existir en la respuesta |

**Ejemplo:**
```python
# Con JSON body
api.post("/users", json={"name": "Alice", "email": "alice@example.com"})

# Con form data
api.post("/login", data={"username": "alice", "password": "secret"})

# Verificar respuesta
api.post("/users", json={"name": "Bob"}, expected_json={"id": 2, "name": "Bob"})
```

---

#### `put(path, status=200, json=None, expected_json=None, keys=None, data=None, params=None, headers=None)`

Realiza una petición PUT.

**Parámetros:** Iguales a `post()`

**Ejemplo:**
```python
api.put("/users/1", json={"name": "Alice Updated"})
```

---

#### `patch(path, status=200, json=None, expected_json=None, keys=None, data=None, params=None, headers=None)`

Realiza una petición PATCH.

**Parámetros:** Iguales a `post()`

**Ejemplo:**
```python
api.patch("/users/1", json={"name": "Partial Update"})
```

---

#### `delete(path, status=204, expected_json=None, keys=None, params=None, headers=None)`

Realiza una petición DELETE.

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `path` | str | *requerido* | Ruta del endpoint |
| `status` | int | 204 | Código de estado esperado |

**Ejemplo:**
```python
api.delete("/users/1", status=204)
```

---

### Método de Cleanup

#### `close()`

Cierra el event loop interno. Recomendado llamar al finalizar.

```python
api = ASGITest(app)
# ... tests ...
api.close()
```

---

### Ejemplo Completo

```python
from fastapi import FastAPI
from rapidtest import ASGITest

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"id": user_id, "name": f"User {user_id}"}

@app.post("/users")
def create_user(user: dict):
    return {"id": 1, **user}

# Testing
api = ASGITest(app)
api.get("/users/1", status=200)
api.get("/users/1", expected_json={"id": 1, "name": "User 1"})
api.post("/users", json={"name": "Alice"}, status=201)
api.close()
```

**Output:**
```
✅ 1. PASSED
✅ 2. PASSED
✅ 3. PASSED

time: 0.01 s
```

---

## HTTPTest

Testing via HTTP real a un servidor externo.

```python
from rapidtest import HTTPTest

api = HTTPTest("https://api.example.com")
```

### Constructor

```python
HTTPTest(url, timeout=30)
```

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `url` | str | *requerido* | Base URL del servidor |
| `timeout` | int | 30 | Timeout en segundos |

### Métodos HTTP

Todos los métodos tienen la misma firma y parámetros que `ASGITest`.

**Ejemplo:**
```python
api = HTTPTest("https://jsonplaceholder.typicode.com")

# GET request
api.get("/posts/1", status=200)

# POST request
api.post("/posts", json={"title": "Test", "body": "Content", "userId": 1})

# PUT request
api.put("/posts/1", json={"id": 1, "title": "Updated", "body": "New", "userId": 1})

# PATCH request
api.patch("/posts/1", json={"title": "Patched"})

# DELETE request
api.delete("/posts/1", status=200)
```

---

## Performance

Load testing con múltiples usuarios concurrentes usando threads.

```python
from rapidtest import Performance

perf = Performance(
    base_url="https://api.example.com",
    users=10,
    duration=10
)
```

### Constructor

```python
Performance(*, base_url=None, users=10, duration=10, timeout=10, delay=0.1)
```

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `base_url` | str | None | URL base del servidor |
| `users` | int | 10 | Número de usuarios concurrentes |
| `duration` | int | 10 | Duración del test en segundos |
| `timeout` | int | 10 | Timeout de requests en segundos |
| `delay` | float | 0.1 | Delay entre requests en segundos |

### Métodos

#### `add_task(*, endpoint, method="GET", params=None, headers=None, json=None, data=None)`

Agrega una tarea de request al test.

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `endpoint` | str | *requerido* | Ruta del endpoint |
| `method` | str | "GET" | Método HTTP |
| `params` | dict | None | Query parameters |
| `headers` | dict | None | Headers HTTP |
| `json` | dict | None | Body JSON |
| `data` | dict | None | Form data |

**Ejemplo:**
```python
perf = Performance(base_url="https://api.example.com", users=10, duration=5)

perf.add_task(endpoint="/health", method="GET")
perf.add_task(endpoint="/users", method="GET")
perf.add_task(endpoint="/users", method="POST", json={"name": "Test"})

results = perf.run()
```

---

#### `run() -> dict`

Ejecuta el test de carga y retorna resultados.

**Retorna:** Dictionary con métricas:
- `total_requests`: Total de requests ejecutados
- `successful_requests`: Requests exitosos (2xx-3xx)
- `failed_requests`: Requests fallidos
- `success_rate`: Porcentaje de éxito
- `avg_response_time`: Tiempo promedio de respuesta (ms)
- `min_response_time`: Tiempo mínimo (ms)
- `max_response_time`: Tiempo máximo (ms)
- `requests_per_second`: Requests por segundo

**Ejemplo:**
```python
results = perf.run()
print(f"RPS: {results['requests_per_second']}")
```

---

## Data

Generador de datos fake usando Faker.

```python
from rapidtest import Data

user = Data.generate_user()
```

### Métodos de Usuario

#### `generate_user(fields=None) -> dict`

Genera un diccionario con datos de usuario.

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `fields` | list | Lista de campos a incluir. None = todos |

**Campos disponibles:** `id`, `name`, `username`, `password`, `email`, `age`, `address`, `phone`, `city`, `state`, `country`, `company`

**Ejemplo:**
```python
# Todos los campos
user = Data.generate_user()

# Solo algunos campos
user = Data.generate_user(['name', 'email', 'password'])
```

---

#### `generate_auth_user() -> dict`

Genera username y password.

```python
auth = Data.generate_auth_user()
# {'username': 'alice123', 'password': 'xJ9#kL2m'}
```

---

#### `generate_users(count, fields=None) -> list[dict]`

Genera múltiples usuarios.

```python
users = Data.generate_users(5)
users = Data.generate_users(3, ['name', 'email'])
```

---

### Métodos Individuales

| Método | Descripción |
|--------|-------------|
| `generate_name()` | Nombre completo |
| `generate_email()` | Email |
| `generate_password()` | Password seguro |
| `generate_phone()` | Teléfono |
| `generate_address()` | Dirección |
| `generate_city()` | Ciudad |
| `generate_state()` | Estado/Provincia |
| `generate_country()` | País |
| `generate_zipcode()` | Código postal |
| `generate_id()` | UUID |
| `generate_job()` | Título de trabajo |
| `generate_text()` | Texto corto |
| `generate_paragraph()` | Párrafo largo |
| `generate_date()` | Fecha (ISO) |
| `generate_datetime()` | Fecha y hora (ISO) |
| `generate_time()` | Hora |
| `generate_url()` | URL |
| `generate_domain()` | Dominio |
| `generate_ipv4()` | Dirección IPv4 |
| `generate_company()` | Nombre de empresa |
| `generate_company_email()` | Email de empresa |
| `generate_product_name()` | Nombre de producto |
| `generate_price(min, max)` | Precio |

### Locale

#### `set_locale(locale)`

Cambia el locale para generación de datos.

```python
Data.set_locale("es_ES")  # Datos en español
Data.set_locale("en_US")  # Datos en inglés americano
Data.set_locale("fr_FR")  # Datos en francés
```

#### `reset_locale()`

Resetea al locale por defecto (en_US).

```python
Data.reset_locale()
```

---

## StatusCode

Enum con códigos de estado HTTP.

```python
from rapidtest import StatusCode, ASGITest

api = ASGITest(app)
api.get("/users", status=StatusCode.OK_200)
```

### Códigos Comunes

| Enum | Valor | Descripción |
|------|-------|-------------|
| `OK_200` | 200 | OK |
| `CREATED_201` | 201 | Created |
| `NO_CONTENT_204` | 204 | No Content |
| `BAD_REQUEST_400` | 400 | Bad Request |
| `UNAUTHORIZED_401` | 401 | Unauthorized |
| `FORBIDDEN_403` | 403 | Forbidden |
| `NOT_FOUND_404` | 404 | Not Found |
| `INTERNAL_SERVER_ERROR_500` | 500 | Internal Server Error |

### Métodos de Verificación

```python
code = StatusCode.OK_200

code.is_success()         # True (2xx)
code.is_client_error()    # False
code.is_server_error()    # False
code.is_error()           # False
code.category              # "Success"
code.reason               # "OK"
```

---

## Uso Rápido (Quick Start)

```python
from fastapi import FastAPI
from rapidtest import ASGITest, Data

# Crear app de test
app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"id": user_id, "name": f"User {user_id}"}

@app.post("/users")
def create_user(user: dict):
    return {"id": 1, **user}

# Testing
api = ASGITest(app)

# Generar datos fake
user_data = Data.generate_user(['name', 'email'])

# Tests
api.get("/users/1", status=200, keys=["id", "name"])
api.post("/users", json=user_data, status=201)

api.close()
```

**Output:**
```
✅ 1. PASSED
✅ 2. PASSED

time: 0.02 s
```