# Tutorial: Performance Testing

Aprende a realizar pruebas de carga y estrés con `Performance`. Esta clase te permite simular múltiples usuarios concurrentes para evaluar el rendimiento de tu API.

## ¿Qué es Performance Testing?

El módulo `Performance` de RapidTest te permite:
- Simular múltiples usuarios concurrentes
- Medir tiempos de respuesta
- Calcular tasa de éxito
- Evaluar throughput (requests por segundo)

## Configuración Inicial

```python
from rapidtest import Performance

# Crear instancia
perf = Performance(
    base_url="http://localhost:8000",
    users=10,        # Usuarios concurrentes
    duration=10,     # Duración en segundos
    timeout=10,     # Timeout por request
    delay=0.1       # Delay entre requests
)
```

## Parámetros del Constructor

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `base_url` | str | None | URL base de la API |
| `users` | int | 10 | Número de usuarios concurrentes |
| `duration` | int | 10 | Duración de la prueba en segundos |
| `timeout` | int | 10 | Timeout máximo por request |
| `delay` | float | 0.1 | Delay entre requests |

## Añadir Tareas de Prueba

Usa el método `add_task()` para definir los endpoints a probar:

```python
# GET request simple
perf.add_task(endpoint="/health", method="GET")

# GET con parámetros
perf.add_task(
    endpoint="/users",
    method="GET",
    params={"page": 1}
)

# POST request
perf.add_task(
    endpoint="/login",
    method="POST",
    json={"username": "test", "password": "test123"}
)

# PUT request
perf.add_task(
    endpoint="/users/1",
    method="PUT",
    json={"name": "Updated"}
)

# DELETE request
perf.add_task(endpoint="/users/1", method="DELETE")

# Con headers
perf.add_task(
    endpoint="/protected",
    method="GET",
    headers={"Authorization": "Bearer token"}
)
```

## Ejecutar la Prueba

```python
results = perf.run()
print(results)
```

## Métricas Devueltas

El método `run()` retorna un diccionario con:

```python
{
    'total_requests': 1500,        # Total de requests realizados
    'successful_requests': 1485,  # Requests exitosos
    'failed_requests': 15,         # Requests fallidos
    'success_rate': 99.0,          # Porcentaje de éxito
    'avg_response_time': 45.2,     # Tiempo promedio en ms
    'min_response_time': 12.1,    # Tiempo mínimo en ms
    'max_response_time': 89.7,    # Tiempo máximo en ms
    'requests_per_second': 150.0, # Requests por segundo
    'duration': 10,                # Duración real en segundos
    'users': 10                   # Usuarios concurrentes
}
```

## Ejemplo Completo: Prueba de Carga

```python
from rapidtest import Performance

# Configurar prueba de carga
perf = Performance(
    base_url="http://localhost:8000",
    users=50,          # 50 usuarios concurrentes
    duration=30,      # 30 segundos
    timeout=15,       # 15 segundos de timeout
    delay=0.2         # 200ms entre requests
)

# Añadir tareas
print("Configurando pruebas de carga...")

# Prueba del endpoint de salud
perf.add_task(endpoint="/health", method="GET")

# Prueba de listado de usuarios
perf.add_task(endpoint="/users", method="GET")

# Prueba de creación de usuario
perf.add_task(
    endpoint="/users",
    method="POST",
    json={"name": "Load Test User", "email": "load@test.com"}
)

# Ejecutar prueba
print("\n🚀 Iniciando prueba de carga...\n")
results = perf.run()

# Analizar resultados
print("\n📊 RESUMEN DE RESULTADOS:")
print(f"   Éxito: {results['success_rate']}%")
print(f"   Throughput: {results['requests_per_second']} req/s")
print(f"   Tiempo promedio: {results['avg_response_time']}ms")
```

## Ejemplo: Validación de Resultados

```python
from rapidtest import Performance

def run_and_validate():
    perf = Performance(
        base_url="http://localhost:8000",
        users=100,
        duration=60,
        timeout=10
    )
    
    perf.add_task(endpoint="/api/health", method="GET")
    results = perf.run()
    
    # Validaciones
    assert results['success_rate'] >= 95, f"Tasa de éxito muy baja: {results['success_rate']}%"
    assert results['avg_response_time'] <= 500, f"Tiempo promedio muy alto: {results['avg_response_time']}ms"
    assert results['requests_per_second'] >= 10, f"Throughput muy bajo: {results['requests_per_second']}"
    
    print(f"✅ Todas las validaciones pasaron!")
    return results

run_and_validate()
```

## Ejemplo: Múltiples Escenarios

```python
from rapidtest import Performance

def test_api_endpoints():
    scenarios = [
        {
            "name": "Health Check",
            "endpoint": "/health",
            "method": "GET",
            "expected_success_rate": 99,
            "max_response_time": 200
        },
        {
            "name": "User List",
            "endpoint": "/users",
            "method": "GET",
            "expected_success_rate": 95,
            "max_response_time": 500
        },
        {
            "name": "User Creation",
            "endpoint": "/users",
            "method": "POST",
            "json": {"name": "Test", "email": "test@example.com"},
            "expected_success_rate": 90,
            "max_response_time": 1000
        }
    ]
    
    for scenario in scenarios:
        print(f"\n🧪 Probando: {scenario['name']}")
        
        perf = Performance(
            base_url="http://localhost:8000",
            users=20,
            duration=10
        )
        
        perf.add_task(
            endpoint=scenario["endpoint"],
            method=scenario["method"],
            json=scenario.get("json")
        )
        
        results = perf.run()
        
        # Validar contra expectativas
        if results['success_rate'] < scenario['expected_success_rate']:
            print(f"   ⚠️  Advertencia: tasa de éxito {results['success_rate']}% < {scenario['expected_success_rate']}%")
        
        if results['avg_response_time'] > scenario['max_response_time']:
            print(f"   ⚠️  Advertencia: tiempo {results['avg_response_time']}ms > {scenario['max_response_time']}ms")

test_api_endpoints()
```

## Interpretación de Resultados

| Indicador | Valor Ideal | Significado |
|-----------|-------------|-------------|
| `success_rate` | ≥ 95% | La API es estable |
| `avg_response_time` | ≤ 500ms | Buenos tiempos de respuesta |
| `requests_per_second` | Alto | Mayor throughput |
| `max_response_time` | ≤ 2x promedio | Sin outliers significativos |

## Consejos para Pruebas Efectivas

1. **Empieza gradualmente**: Comienza con pocos usuarios y ve aumentando
2. **Mide el baseline**: Primero establece un punto de referencia
3. **Aísla endpoints**: Prueba un endpoint a la vez para resultados claros
4. **Considera el delay**: Un delay muy bajo puede saturar el servidor
5. **Monitorea el servidor**: Observa CPU, memoria y conexiones de la API

## Siguiente Paso

¿Ya dominas las pruebas básicas? Explora más en:
- [Advanced Examples](../examples/advanced.md)
- [API Reference](../api/performance.md)