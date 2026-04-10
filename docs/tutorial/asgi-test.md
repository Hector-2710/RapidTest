# Tutorial: ASGI Testing

Aprende a probar aplicaciones ASGI directamente, sin necesidad de iniciar un servidor HTTP. Esto hace que las pruebas sean más rápidas y fáciles de configurar.

## ¿Qué es ASGI Testing?

`ASGITest` te permite probar tu aplicación (FastAPI, Starlette, etc.) directamente ejecutándola en memoria, sin necesidad de levantar un servidor.

**Ventajas:**
- ⚡ Más rápido - no necesita servidor
- 🔧 Más fácil de configurar
- 🧪 Ideal para unit tests
- 🎯 Funciona con cualquier app ASGI

## Configuración Inicial

```python
from rapidtest import ASGITest
from tu_app import app  # Tu aplicación FastAPI/Starlette

# Inicializar el tester con tu app
api = ASGITest(app=app)
```

## Métodos HTTP Disponibles

Los mismos métodos que HTTPTest están disponibles:

### GET

```python
# Solicitud básica
api.get(path="/", status=200)

# Con parámetros
api.get(path="/users", params={"page": 1}, status=200)

# Con headers
api.get(
    path="/health",
    headers={"X-Custom": "value"},
    status=200
)

# Validar respuesta JSON
api.get(
    path="/users/1",
    expected_json={"id": 1, "name": "John"},
    status=200
)
```

### POST

```python
# Enviar JSON
api.post(
    path="/users",
    json={"name": "Jane", "email": "jane@example.com"},
    status=201
)

# Con formulario
api.post(
    path="/login",
    data={"username": "john", "password": "secret"},
    status=200
)
```

### PUT, PATCH, DELETE

```python
# PUT - Reemplazo completo
api.put(
    path="/users/1",
    json={"name": "Updated", "email": "updated@example.com"},
    status=200
)

# PATCH - Actualización parcial
api.patch(
    path="/users/1",
    json={"name": "New Name"},
    status=200
)

# DELETE - Eliminar
api.delete(path="/users/1", status=204)
```

## Ejemplo Completo: Testing de FastAPI

### Tu aplicación (app.py)

```python
# app.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"id": user_id, "name": f"User {user_id}"}

@app.post("/users")
def create_user(user: dict):
    user["id"] = 1
    return user
```

### Pruebas con ASGITest

```python
# test_app.py
from fastapi import FastAPI
from rapidtest import ASGITest

# Crear la app
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"id": user_id, "name": f"User {user_id}"}

@app.post("/users")
def create_user(user: dict):
    user["id"] = 1
    return user

# === PRUEBAS ===

api = ASGITest(app=app)

print("1. Testing health endpoint...")
api.get(path="/health", status=200, keys=["status"])

print("\n2. Testing user detail...")
api.get(path="/users/5", status=200, expected_json={"id": 5, "name": "User 5"})

print("\n3. Testing user creation...")
api.post(
    path="/users",
    json={"name": "John", "email": "john@example.com"},
    status=201,
    keys=["id"]
)

print("\n4. Testing root endpoint...")
api.get(path="/", status=200, expected_json={"message": "Hello World"})

# Cerrar el loop de eventos al final
api.close()
```

## Diferencias entre HTTPTest y ASGITest

| Aspecto | HTTPTest | ASGITest |
|---------|----------|----------|
| **Servidor** | Requiere servidor corriendo | No requiere servidor |
| **Velocidad** | Más lento | Más rápido |
| **Use case** | Pruebas de integración | Pruebas unitarias |
| **Configuración** | needs URL del servidor | Solo la app |
| **Import** | `from rapidtest import HTTPTest` | `from rapidtest import ASGITest` |

## Integración con pytest

```python
# conftest.py
import pytest
from fastapi import FastAPI
from rapidtest import ASGITest

@pytest.fixture
def app():
    return FastAPI()

@pytest.fixture
def api(app):
    tester = ASGITest(app=app)
    yield tester
    tester.close()

# test_api.py
def test_health(api):
    api.get(path="/health", status=200)

def test_create_user(api):
    api.post(
        path="/users",
        json={"name": "Test"},
        status=201
    )
```

## Manejo de Errores

```python
from fastapi import FastAPI
from rapidtest import ASGITest

app = FastAPI()

@app.get("/item/{item_id}")
def get_item(item_id: int):
    if item_id == 404:
        raise HTTPException(status_code=404, detail="Not found")
    return {"id": item_id}

api = ASGITest(app=app)

# Probar error 404
api.get(path="/item/404", status=404)
```

## Notas Importantes

1. **Cerrar recursos**: Al terminar las pruebas, llama `api.close()` para cerrar el event loop.

2. **Scope ASGI**: El scope creado es de tipo "http" básico. Si tu app depende de WebSockets u otras características avanzadas, puede que no funcione igual.

3. **Headers**: Los headers se convierten a minúsculas automáticamente (según especificación ASGI).

## Siguiente Paso

¿Necesitas hacer pruebas de carga? Aprende sobre [Performance Testing](performance.md).