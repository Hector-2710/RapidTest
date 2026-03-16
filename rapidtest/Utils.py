from typing import Any
import json

def encode_query_params(params: dict[str, Any]) -> bytes:
    if not params:
        return b""
    return "&".join(f"{k}={v}" for k, v in params.items()).encode()

def encode_headers(headers: dict[str, str]) -> list[tuple[bytes, bytes]]:
    return [(key.lower().encode(), value.encode()) for key, value in headers.items()]

def decode_headers(headers: list[tuple[bytes, bytes]]) -> list[tuple[str, str]]:
    return [(key.decode(), value.decode()) for key, value in headers]

def try_parse_json(content: bytes) -> dict[str, Any] | None:
    try:
        return json.loads(content.decode())
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None

def validate_contain_keys(response_json: dict[str, Any] | None, contain_keys: list[str]) -> bool:
    if not response_json:
        return False

    for item in contain_keys:
        if item not in response_json:
            return False
    return True

def parse_response_body(response: Any) -> dict[str, Any]:
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
    GREEN = '\033[92m'  
    RED = '\033[91m'    
    BLUE = '\033[96m'   
    YELLOW = '\033[93m' 
    BOLD = '\033[1m'    
    RESET = '\033[0m'   

    if result == "PASSED":
        color = GREEN
        icon = "✅"
    else:
        color = RED
        icon = "❌"
    
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
    RED = '\033[91m'    
    BLUE = '\033[96m'   
    YELLOW = '\033[93m' 
    BOLD = '\033[1m'    
    RESET = '\033[0m'   
    
    print()
    print(f"{RED}{BOLD}🔥 CRITICAL API ERROR{RESET}")
    print(f"{BOLD}URL:{RESET} {BLUE}{url}{RESET}")
    print(f"{BOLD}Error Type:{RESET} {YELLOW}{type(exception).__name__}{RESET}")
    print(f"{BOLD}Error Message:{RESET} {RED}{str(exception)}{RESET}")
    
    if hasattr(exception, 'response') and exception.response is not None:
        print(f"{BOLD}HTTP Status:{RESET} {RED}{exception.response.status_code}{RESET}")
        print(f"{BOLD}Response Headers:{RESET} {dict(exception.response.headers)}")
    
    print()
    
   