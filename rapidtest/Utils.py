from typing import Any, Optional
import json

def print_report(result: str, url: str, status: int, body: Any, error_msg: Optional[str] = None) -> None:
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
    
    def _calculate_results(results, duration, users) -> Dict[str, Any]:
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