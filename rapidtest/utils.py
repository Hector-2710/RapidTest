import atexit
import json
from typing import Any

_simple_report_buffer: list[str] = []

GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[96m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"


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


def validate_contain_keys(json: dict[str, Any] | None, keys: list[str]) -> bool:
    if not json:
        return False
    return all(key in json for key in keys)


def parse_response_body(response: Any) -> dict[str, Any]:
    try:
        parsed = response.json()
        return parsed if parsed is not None else {"raw_content": None}
    except json.JSONDecodeError:
        if hasattr(response, "text"):
            return {"raw_content": response.text}

        return {"raw_content": str(getattr(response, "content", ""))}


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
    response: Any,
    url: str,
    expected_status: int,
    expected_json: dict[str, Any] | None = None,
    contain_keys: list[str] | None = None,
    simple_report: bool = False,
) -> bool:
    response_json = parse_response_body(response)
    keys_ok = (
        validate_contain_keys(response_json, contain_keys) if contain_keys else True
    )

    status_ok = response.status_code == expected_status
    body_ok = expected_json is None or response_json == expected_json

    result = "PASSED" if (status_ok and body_ok and keys_ok) else "FAILED"

    if simple_report:
        print_report_simple(result)
    else:
        error_msg = _build_error_message(
            status_ok, keys_ok, expected_status, response.status_code
        )
        print_report(result, url, response.status_code, response_json, error_msg)

    return status_ok and body_ok and keys_ok


def print_report(
    result: str, url: str, status: int, body: Any, error_msg: str | None = None
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

    if error_msg:
        print(f"{RED}{BOLD}Error:{RESET} {error_msg}")

    if body:
        print(f"{BLUE}Response Body:{RESET}")
        if isinstance(body, (dict, list)):
            print(json.dumps(body, indent=2))
        else:
            print(str(body))

    print("=" * 60)


def print_report_simple(result: str) -> None:
    if result == "PASSED":
        icon = "✅"
    else:
        icon = "❌"

    _simple_report_buffer.append(
        f"{GREEN if result == 'PASSED' else RED}{BOLD}{icon} {result}{RESET}"
    )


def flush_simple_report_buffer() -> None:
    """Prints all buffered simple report entries at once and clears the buffer."""
    if not _simple_report_buffer:
        return

    print()
    for item in _simple_report_buffer:
        print(item)
    _simple_report_buffer.clear()


atexit.register(flush_simple_report_buffer)


def show_connection_error(url: str, exception: Exception) -> None:
    print()
    print(f"{RED}{BOLD}🔥 CRITICAL API ERROR{RESET}")
    print(f"{BOLD}URL:{RESET} {BLUE}{url}{RESET}")
    print(f"{BOLD}Error Type:{RESET} {YELLOW}{type(exception).__name__}{RESET}")
    print(f"{BOLD}Error Message:{RESET} {RED}{str(exception)}{RESET}")

    if hasattr(exception, "response") and exception.response is not None:
        print(f"{BOLD}HTTP Status:{RESET} {RED}{exception.response.status_code}{RESET}")
        print(f"{BOLD}Response Headers:{RESET} {dict(exception.response.headers)}")

    print()
