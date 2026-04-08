import json
from typing import Any

_simple_report_buffer: list[tuple[int, str]] = []

GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[96m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"


def try_parse_json(content: bytes) -> dict[str, Any] | None:
    try:
        return json.loads(content.decode())
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None


def validate_contain_keys(data: dict[str, Any] | None, keys: list[str]) -> bool:
    if not data:
        return False
    return all(key in data for key in keys)


def _build_error_message(
    status_ok: bool,
    keys_ok: bool,
    expected_status: int,
    actual_status: int,
) -> str | None:
    if status_ok and keys_ok:
        return None
    if status_ok:
        return "Response body or keys mismatch"
    return f"Expected status {expected_status}, got {actual_status}"


def validate_and_report_response(
    response_json: dict[str, Any] | None,
    status_code: int,
    url: str,
    expected_status: int,
    expected_json: dict[str, Any] | None = None,
    contain_keys: list[str] | None = None,
    simple_report: bool = False,
    elapsed_ms: float | None = None,
) -> bool:
    keys_ok = (
        validate_contain_keys(response_json, contain_keys) if contain_keys else True
    )
    status_ok = status_code == expected_status
    body_ok = expected_json is None or response_json == expected_json

    result = "PASSED" if (status_ok and body_ok and keys_ok) else "FAILED"

    if simple_report:
        pass
        #
    else:
        error_msg = _build_error_message(
            status_ok, keys_ok, expected_status, status_code
        )
        print_report(result, url, status_code, response_json, error_msg, elapsed_ms)

    return status_ok and body_ok and keys_ok


def print_report(
    result: str,
    url: str,
    status: int,
    body: Any,
    error_msg: str | None = None,
    elapsed_ms: float | None = None,
) -> None:
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
    if elapsed_ms is not None:
        print(f"{BLUE}Time:{RESET} {elapsed_ms:.2f}ms")

    if error_msg:
        print(f"{RED}{BOLD}Error:{RESET} {error_msg}")

    if body:
        print(f"{BLUE}Response Body:{RESET}")
        if isinstance(body, (dict, list)):
            print(json.dumps(body, indent=2))
        else:
            print(str(body))

    print("=" * 60)

def show_connection_error(url: str, exception: Exception) -> None:
    print()
    print(f"{RED}{BOLD}🔥 CRITICAL API ERROR{RESET}")
    print(f"{BOLD}URL:{RESET} {BLUE}{url}{RESET}")
    print(f"{BOLD}Error Type:{RESET} {YELLOW}{type(exception).__name__}{RESET}")
    print(f"{BOLD}Error Message:{RESET} {RED}{str(exception)}{RESET}")
    print()
