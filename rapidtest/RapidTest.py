import requests
from typing import Optional, Dict, Any
from rapidtest.Utils import print_report


class Test:
    """
    Clase principal para realizar pruebas de integración en APIs REST.
    
    Esta clase permite realizar peticiones HTTP y validar automáticamente 
    el código de estado y el cuerpo de la respuesta.
    """

    def __init__(self, url: str):
        """
        Inicializa el cliente de pruebas.

        Args:
            url (str): La URL base de la API (ej: 'http://localhost:8000').
        """
        self.url = url.rstrip('/')

    def _request(
        self, 
        method: str, 
        endpoint: str, 
        expected_status: int = 200, 
        expected_body: Optional[Dict[str, Any]] = None, 
        **kwargs
    ) -> Optional[requests.Response]:
        """
        Método interno para realizar peticiones y validar resultados.

        Args:
            method (str): Método HTTP (GET, POST, etc.).
            endpoint (str): Ruta del endpoint (ej: '/users').
            expected_status (int): Código de estado HTTP esperado.
            expected_body (dict, optional): Cuerpo JSON esperado en la respuesta.
            **kwargs: Argumentos adicionales para requests (headers, json, params, etc.).

        Returns:
            requests.Response: El objeto de respuesta si la conexión fue exitosa.
            None: Si ocurrió un error crítico de conexión.
        """
        url = f"{self.url}/{endpoint.lstrip('/')}"
        method_func = getattr(requests, method.lower())
        
        try:
            response = method_func(url, **kwargs)
            status_ok = response.status_code == expected_status
            body_ok = True
            error_msg = None
            
            response_json = None
            try:
                response_json = response.json()
            except Exception:
                response_json = {"raw_content": response.text}

            if expected_body is not None:
                if response_json != expected_body:
                    body_ok = False
                    if status_ok:
                        error_msg = "Body mismatch."
                    else:
                        error_msg = f"Expected status {expected_status}, but got {response.status_code} and body mismatch."

            if not status_ok and not error_msg:
                error_msg = f"Expected status {expected_status}, but got {response.status_code}"

            if status_ok and body_ok:
                print_report("PASSED", response.url, response.status_code, response_json)
            else:
                print_report("FAILED", response.url, response.status_code, response_json, error_msg=error_msg)

            return response
            
        except Exception as e:
            print(f"\n❌ CRITICAL ERROR connecting to {url}: {str(e)}")
            return None

    def get(self, endpoint: str, expected_status: int = 200, expected_body: Optional[Dict[str, Any]] = None, **kwargs) -> Optional[requests.Response]:
        """Realiza una petición GET y valida el resultado."""
        return self._request("GET", endpoint, expected_status, expected_body, **kwargs)

    def post(self, endpoint: str, expected_status: int = 200, expected_body: Optional[Dict[str, Any]] = None, **kwargs) -> Optional[requests.Response]:
        """Realiza una petición POST y valida el resultado."""
        return self._request("POST", endpoint, expected_status, expected_body, **kwargs)

    def put(self, endpoint: str, expected_status: int = 200, expected_body: Optional[Dict[str, Any]] = None, **kwargs) -> Optional[requests.Response]:
        """Realiza una petición PUT y valida el resultado."""
        return self._request("PUT", endpoint, expected_status, expected_body, **kwargs)

    def patch(self, endpoint: str, expected_status: int = 200, expected_body: Optional[Dict[str, Any]] = None, **kwargs) -> Optional[requests.Response]:
        """Realiza una petición PATCH y valida el resultado."""
        return self._request("PATCH", endpoint, expected_status, expected_body, **kwargs)

    def delete(self, endpoint: str, expected_status: int = 200, expected_body: Optional[Dict[str, Any]] = None, **kwargs) -> Optional[requests.Response]:
        """Realiza una petición DELETE y valida el resultado."""
        return self._request("DELETE", endpoint, expected_status, expected_body, **kwargs)


    