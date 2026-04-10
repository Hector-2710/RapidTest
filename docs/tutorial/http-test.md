# Tutorial: HTTP Testing

Aprende a probar APIs HTTP tradicionales con `HTTPTest`. Esta clase es ideal cuando necesitas probar un servidor que ya está corriendo.

## Requisitos

- Un servidor API funcionando (local o remoto)
- Instalar RapidTest: `pip install rapidtest`

## Configuración Inicial

```python
from rapidtest import HTTPTest

# Conectar a tu API
api = HTTPTest(url="http://localhost:8000", timeout=30)
```

## Métodos HTTP Disponibles

### GET - Obtener datos

```python
# Solicitud básica
api.get(path="/users", status=200)

# Con parámetros de consulta
api.get(
    path="/users",
    params={"page": 1, "limit": 10},
    status=200
)

# Con headers
api.get(
    path="/protected",
    headers={"Authorization": "Bearer token123"},
    status=200
)

# Validar respuesta JSON
api.get(
    path="/users/1",
    expected_json={"id": 1, "name": "John"},
    status=200
)

# Validar que la respuesta contenga ciertas claves
api.get(
    path="/users/1",
    keys=["id", "name", "email"],
    status=200
)
```

### POST - Crear recursos

```python
# Enviar JSON
new_user = {"name": "Jane", "email": "jane@example.com"}
api.post(
    path="/users",
    json=new_user,
    status=201
)

# Enviar datos de formulario
api.post(
    path="/login",
    data={"username": "john", "password": "secret"},
    status=200
)

# Con validación de respuesta
api.post(
    path="/users",
    json={"name": "Jane"},
    status=201,
    expected_json={"id": 1, "name": "Jane"}
)
```

### PUT - Reemplazar recursos

```python
# Actualización completa
api.put(
    path="/users/1",
    json={"name": "John Updated", "email": "john@example.com"},
    status=200
)
```

### PATCH - Actualización parcial

```python
# Actualización parcial
api.patch(
    path="/users/1",
    json={"email": "newemail@example.com"},
    status=200
)
```

### DELETE - Eliminar recursos

```python
# Eliminar un recurso
api.delete(path="/users/1", status=204)
```

## Ejemplo Completo: CRUD de Usuarios

```python
from rapidtest import HTTPTest, Data

api = HTTPTest(url="http://localhost:8000")

# CREATE - Crear usuario
new_user = {
    "name": Data.generate_name(),
    "email": Data.generate_email(),
    "age": 25
}
response = api.post(path="/users", json=new_user, status=201)
user_id = response.json()["id"]
print(f"Usuario creado: {user_id}")

# READ - Obtener usuario
api.get(path=f"/users/{user_id}", status=200)

# UPDATE - Actualizar usuario
api.patch(
    path=f"/users/{user_id}",
    json={"name": "Nuevo Nombre"},
    status=200
)

# DELETE - Eliminar usuario
api.delete(path=f"/users/{user_id}", status=204)
```

## Manejo de Errores

```python
from rapidtest import HTTPTest

api = HTTPTest(url="http://localhost:8000")

# Probar errores comunes
api.get(path="/users/999999", status=404)  # No encontrado

api.post(
    path="/users",
    json={"email": "invalid-email"},  # Email inválido
    status=400  # Bad Request
)

api.get(path="/admin", status=401)  # No autorizado
```

## Integración con unittest

```python
import unittest
from rapidtest import HTTPTest

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.api = HTTPTest(url="http://localhost:8000")
    
    def test_health_check(self):
        self.api.get(path="/health", status=200)
    
    def test_create_user(self):
        response = self.api.post(
            path="/users",
            json={"name": "Test"},
            status=201
        )
        self.assertIsNotNone(response)

if __name__ == "__main__":
    unittest.main()
```

## Resumen de Parámetros

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `path` | Endpoint de la API | `/users/1` |
| `status` | Código de estado esperado | `200`, `201`, `404` |
| `expected_json` | JSON exacto esperado en respuesta | `{"id": 1}` |
| `keys` | Claves que deben existir en la respuesta | `["id", "name"]` |
| `params` | Parámetros de consulta | `{"page": 1}` |
| `headers` | Headers HTTP | `{"Auth": "Bearer..."}` |
| `json` | Cuerpo JSON para POST/PUT/PATCH | `{"name": "John"}` |
| `data` | Datos de formulario | `{"user": "john"}` |

## Siguiente Paso

¿Necesitas probar tu app directamente sin iniciar un servidor? Aprende sobre [ASGITest](asgi-test.md).