from typing import Any
import json
import statistics
import enum


class StatusCode(enum.IntEnum):
    CONTINUE_100 = 100
    OK_200 = 200
    CREATED_201 = 201
    ACCEPTED_202 = 202
    NO_CONTENT_204 = 204
    MOVED_PERMANENTLY_301 = 301
    TEMPORARY_REDIRECT_307 = 307
    PERMANENT_REDIRECT_308 = 308
    BAD_REQUEST_400 = 400
    UNAUTHORIZED_401 = 401
    FORBIDDEN_403 = 403
    NOT_FOUND_404 = 404
    NOT_ACCEPTABLE_406 = 406
    REQUEST_TIMEOUT_408 = 408
    INTERNAL_SERVER_ERROR_500 = 500


def encode_query_params(params: dict[str, Any]) -> bytes:
    """Encode query params to ASGI query_string bytes."""
    if not params:
        return b""
    return "&".join(f"{k}={v}" for k, v in params.items()).encode()


def encode_headers(headers: dict[str, str]) -> list[tuple[bytes, bytes]]:
    """Encode headers to ASGI-compatible byte tuples."""
    return [(key.lower().encode(), value.encode()) for key, value in headers.items()]


def decode_headers(headers: list[tuple[bytes, bytes]]) -> list[tuple[str, str]]:
    """Decode ASGI header tuples to string tuples."""
    return [(key.decode(), value.decode()) for key, value in headers]


def try_parse_json(content: bytes) -> dict[str, Any] | None:
    """Best-effort JSON parser for response payloads."""
    try:
        return json.loads(content.decode())
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None


def validate_contain_keys(response_json: dict[str, Any] | None, contain_keys: list[str]) -> bool:
    """Validate that the parsed response contains the expected keys."""
    if not response_json:
        return False

    for item in contain_keys:
        if item not in response_json:
            return False

    return True


def parse_response_body(response: Any) -> dict[str, Any]:
    """Parse a response body, falling back to raw text when JSON decoding fails."""
    try:
        parsed = response.json()
        return parsed if parsed is not None else {"raw_content": None}
    except Exception:
        if hasattr(response, "text"):
            return {"raw_content": response.text}

        return {"raw_content": str(getattr(response, "content", ""))}


def validate_and_report_response(
    response: Any,
    url: str,
    expected_status: int,
    expected_json: dict[str, Any] | None = None,
    contain_keys: list[str] | None = None,
) -> bool:
    """Validate a response and print the standard test report."""
    response_json = parse_response_body(response)
    keys_ok = True

    if contain_keys is not None:
        keys_ok = validate_contain_keys(response_json, contain_keys)

    status_ok = response.status_code == expected_status
    body_ok = True
    error_msg = None

    if expected_json is not None and response_json != expected_json:
        body_ok = False
        if status_ok:
            error_msg = (
                "The expected JSON is not the correct"
                if keys_ok
                else "The expected JSON is not the correct and keys are not correct"
            )
        else:
            error_msg = (
                f"Expected status {expected_status}, but got {response.status_code} and the expected JSON is not the correct"
                if keys_ok
                else f"Expected status {expected_status}, but got {response.status_code} and the expected JSON is not the correct and keys are not correct"
            )

    if not status_ok and not error_msg:
        error_msg = (
            f"Expected status {expected_status}, but got {response.status_code}"
            if keys_ok
            else f"Expected status {expected_status}, but got {response.status_code} and keys are not correct"
        )

    if status_ok and body_ok:
        if keys_ok:
            print_report("PASSED", url, response.status_code, response_json)
        else:
            print_report("PASSED", url, response.status_code, response_json, error_msg="Keys are not correct")
    else:
        print_report("FAILED", url, response.status_code, response_json, error_msg=error_msg)

    return status_ok and body_ok and keys_ok

def print_report(result: str, url: str, status: int, body: Any, error_msg: str | None = None) -> None:
    """
    Imprime un reporte simple y rápido del resultado de una prueba.

    Args:
        result (str): El resultado de la prueba ('PASSED' o 'FAILED').
        url (str): La URL a la que se realizó la petición.
        status (int): El código de estado HTTP recibido.
        body (any): El cuerpo de la respuesta (usualmente un dict o list).
        error_msg (str, optional): Mensaje detallado del error si la prueba falló.
    """
    
    # Códigos de color ANSI
    GREEN = '\033[92m'  # Verde
    RED = '\033[91m'    # Rojo
    BLUE = '\033[96m'   # Cian
    YELLOW = '\033[93m' # Amarillo
    BOLD = '\033[1m'    # Negrita
    RESET = '\033[0m'   # Reset
    
    # Configuración según el resultado
    if result == "PASSED":
        color = GREEN
        icon = "✅"
    else:
        color = RED
        icon = "❌"
    
    # Status color
    if 200 <= status < 300:
        status_color = GREEN
    elif 400 <= status < 500:
        status_color = YELLOW  
    else:
        status_color = RED
    
    print()
    print(f"{color}{BOLD}{icon} TEST {result}{RESET}")
    print(f"{BLUE}URL:{RESET} {url}")
    print(f"{BLUE}Status:{RESET} {status_color}{status}{RESET}")
    
    if error_msg:
        print(f"{RED}{BOLD}Error:{RESET} {error_msg}")
    
    if body:
        print(f"{BLUE}Response Body:{RESET}")
        if isinstance(body, (dict, list)):
            print(json.dumps(body, indent=2))
        else:
            print(str(body))
    
    print("="*60)


def show_connection_error(url: str, exception: Exception) -> None:
    """
    Muestra un error de conexión simple y claro.
    
    Args:
        url (str): La URL que falló
        exception (Exception): La excepción que ocurrió
    """
    # Códigos de color ANSI
    RED = '\033[91m'    # Rojo
    BLUE = '\033[96m'   # Cian
    YELLOW = '\033[93m' # Amarillo
    BOLD = '\033[1m'    # Negrita
    RESET = '\033[0m'   # Reset
    
    print()
    print(f"{RED}{BOLD}🔥 CRITICAL API ERROR{RESET}")
    print(f"{BOLD}URL:{RESET} {BLUE}{url}{RESET}")
    print(f"{BOLD}Error Type:{RESET} {YELLOW}{type(exception).__name__}{RESET}")
    print(f"{BOLD}Error Message:{RESET} {RED}{str(exception)}{RESET}")
    
    if hasattr(exception, 'response') and exception.response is not None:
        print(f"{BOLD}HTTP Status:{RESET} {RED}{exception.response.status_code}{RESET}")
        print(f"{BOLD}Response Headers:{RESET} {dict(exception.response.headers)}")
    
    print()
    
    def _calculate_results(results, duration, users) -> dict[str, Any]:
        """Calculate and display test results."""
        if not results:
            print("❌ No results collected")
            return {}
            
        # Calculate statistics
        total_requests = len(results)
        successful_requests = sum(1 for r in results if r['success'])
        failed_requests = total_requests - successful_requests
        
        response_times = [r['response_time'] for r in results if r['success']]
        
        if response_times:
            avg_response_time = statistics.mean(response_times)
            min_response_time = min(response_times)
            max_response_time = max(response_times)
        else:
            avg_response_time = min_response_time = max_response_time = 0
            
        rps = total_requests / duration if duration > 0 else 0
        success_rate = (successful_requests / total_requests * 100) if total_requests > 0 else 0
        
        # Create results dictionary
        results = {
            'total_requests': total_requests,
            'successful_requests': successful_requests,
            'failed_requests': failed_requests,
            'success_rate': round(success_rate, 2),
            'avg_response_time': round(avg_response_time, 2),
            'min_response_time': round(min_response_time, 2),
            'max_response_time': round(max_response_time, 2),
            'requests_per_second': round(rps, 2),
            'duration': duration,
            'users': users
        }
        
        # Display results
        print("\n" + "="*60)
        print("📊 PERFORMANCE TEST RESULTS")
        print("="*60)
        print(f"🎯 Total Requests:      {results['total_requests']}")
        print(f"✅ Successful:          {results['successful_requests']}")
        print(f"❌ Failed:              {results['failed_requests']}")
        print(f"📈 Success Rate:        {results['success_rate']}%")
        print(f"⚡ Requests/sec:        {results['requests_per_second']}")
        print(f"⏱️  Avg Response Time:   {results['avg_response_time']}ms")
        print(f"🐌 Min Response Time:   {results['min_response_time']}ms")
        print(f"🐇 Max Response Time:   {results['max_response_time']}ms")
        print(f"👥 Concurrent Users:    {results['users']}")
        print(f"⏰ Test Duration:       {results['duration']}s")
        print("="*60)
        
        # Status indicator
        if results['success_rate'] >= 95:
            print("🟢 Excellent performance!")
        elif results['success_rate'] >= 80:
            print("🟡 Good performance")
        else:
            print("🔴 Poor performance - check server")
            
        return results