"""
HTTPTest: Real HTTP endpoint testing.

Provides testing of HTTP endpoints by making real HTTP requests to a running
server. Uses the requests library for HTTP communication.

Example:
    >>> from rapidtest import HTTPTest
    >>> api = HTTPTest("https://api.example.com")
    >>> api.get("/users/1", status=200)
    >>> api.post("/users", json={"name": "Alice"})
"""

import requests
import time
import atexit
from urllib.parse import urlencode
from .utils import GREEN, RED, BOLD, RESET

_total_tests: int = 0
_total_time: float = 0.0


class HTTPTest:
    """
    HTTP endpoint tester using real requests.

    Tests HTTP endpoints by making actual HTTP requests to a running server.
    Useful for integration testing against deployed APIs.

    Attributes:
        url: Base URL of the server.
        timeout: Request timeout in seconds.
        _counter: Counter for the number of tests run.

    Example:
        >>> api = HTTPTest("https://jsonplaceholder.typicode.com")
        >>> api.get("/posts/1", status=200)
        >>> api.post("/posts", json={"title": "Test", "body": "Content"})
    """

    __slots__ = ("url", "timeout", "_counter")

    def __init__(self, url: str, timeout: int = 30) -> None:
        """
        Initialize HTTPTest with a base URL.

        Args:
            url: Base URL of the server (e.g., "https://api.example.com").
                Trailing slash will be stripped.
            timeout: Request timeout in seconds (default: 30).

        Example:
            >>> api = HTTPTest("https://api.example.com", timeout=60)
        """
        self.url = url.rstrip("/")
        self.timeout = timeout
        self._counter = 0

    def get(
        self,
        path: str,
        status: int = 200,
        expected_json: dict | None = None,
        keys: list | None = None,
        params: dict | None = None,
        headers: dict | None = None,
        **_,
    ) -> requests.Response | None:
        """
        Perform a GET request.

        Args:
            path: URL path (e.g., "/users/1", "/health").
            status: Expected HTTP status code (default: 200).
            expected_json: Exact JSON response expected (optional).
            keys: List of keys that must exist in the response (optional).
            params: Query parameters as a dictionary (optional).
            headers: HTTP headers as a dictionary (optional).
            **_: Ignore additional keyword arguments.

        Returns:
            requests.Response object if successful, None otherwise.

        Example:
            >>> response = api.get("/users/1", status=200)
            >>> api.get("/users", params={"active": True}, keys=["id", "name"])
        """
        return self._exec(
            "GET", path, status, expected_json, keys, params, headers, None
        )

    def post(
        self,
        path: str,
        status: int = 201,
        json: dict | None = None,
        expected_json: dict | None = None,
        keys: list | None = None,
        data: dict | None = None,
        params: dict | None = None,
        headers: dict | None = None,
        **_,
    ) -> requests.Response | None:
        """
        Perform a POST request.

        Args:
            path: URL path (e.g., "/users", "/posts").
            status: Expected HTTP status code (default: 201).
            json: JSON body as a dictionary (optional).
            expected_json: Exact JSON response expected (optional).
            keys: List of keys that must exist in the response (optional).
            data: Form data as a dictionary (optional).
            params: Query parameters (optional).
            headers: HTTP headers (optional).
            **_: Ignore additional keyword arguments.

        Returns:
            requests.Response object if successful, None otherwise.

        Example:
            >>> api.post("/users", json={"name": "Alice", "email": "alice@example.com"})
            >>> api.post("/login", data={"username": "alice", "password": "secret"})
        """
        body = None
        req_headers = dict(headers) if headers else {}
        if json is not None:
            import json as _json

            body = _json.dumps(json)
            req_headers["content-type"] = "application/json"
        elif data is not None:
            body = urlencode(data, doseq=True)
            req_headers["content-type"] = "application/x-www-form-urlencoded"
        return self._exec(
            "POST", path, status, expected_json, keys, params, req_headers, body
        )

    def put(
        self,
        path: str,
        status: int = 200,
        json: dict | None = None,
        expected_json: dict | None = None,
        keys: list | None = None,
        data: dict | None = None,
        params: dict | None = None,
        headers: dict | None = None,
        **_,
    ) -> requests.Response | None:
        """
        Perform a PUT request.

        Args:
            path: URL path (e.g., "/users/1").
            status: Expected HTTP status code (default: 200).
            json: JSON body as a dictionary (optional).
            expected_json: Exact JSON response expected (optional).
            keys: List of keys that must exist in the response (optional).
            data: Form data as a dictionary (optional).
            params: Query parameters (optional).
            headers: HTTP headers (optional).
            **_: Ignore additional keyword arguments.

        Returns:
            requests.Response object if successful, None otherwise.

        Example:
            >>> api.put("/users/1", json={"name": "Updated Name"})
        """
        body = None
        req_headers = dict(headers) if headers else {}
        if json is not None:
            import json as _json

            body = _json.dumps(json)
            req_headers["content-type"] = "application/json"
        elif data is not None:
            body = urlencode(data, doseq=True)
            req_headers["content-type"] = "application/x-www-form-urlencoded"
        return self._exec(
            "PUT", path, status, expected_json, keys, params, req_headers, body
        )

    def patch(
        self,
        path: str,
        status: int = 200,
        json: dict | None = None,
        expected_json: dict | None = None,
        keys: list | None = None,
        data: dict | None = None,
        params: dict | None = None,
        headers: dict | None = None,
        **_,
    ) -> requests.Response | None:
        """
        Perform a PATCH request.

        Args:
            path: URL path (e.g., "/users/1").
            status: Expected HTTP status code (default: 200).
            json: JSON body as a dictionary (optional).
            expected_json: Exact JSON response expected (optional).
            keys: List of keys that must exist in the response (optional).
            data: Form data as a dictionary (optional).
            params: Query parameters (optional).
            headers: HTTP headers (optional).
            **_: Ignore additional keyword arguments.

        Returns:
            requests.Response object if successful, None otherwise.

        Example:
            >>> api.patch("/users/1", json={"name": "Partially Updated"})
        """
        body = None
        req_headers = dict(headers) if headers else {}
        if json is not None:
            import json as _json

            body = _json.dumps(json)
            req_headers["content-type"] = "application/json"
        elif data is not None:
            body = urlencode(data, doseq=True)
            req_headers["content-type"] = "application/x-www-form-urlencoded"
        return self._exec(
            "PATCH", path, status, expected_json, keys, params, req_headers, body
        )

    def delete(
        self,
        path: str,
        status: int = 204,
        expected_json: dict | None = None,
        keys: list | None = None,
        params: dict | None = None,
        headers: dict | None = None,
        **_,
    ) -> requests.Response | None:
        """
        Perform a DELETE request.

        Args:
            path: URL path (e.g., "/users/1").
            status: Expected HTTP status code (default: 204).
            expected_json: Exact JSON response expected (optional).
            keys: List of keys that must exist in the response (optional).
            params: Query parameters (optional).
            headers: HTTP headers (optional).
            **_: Ignore additional keyword arguments.

        Returns:
            requests.Response object if successful, None otherwise.

        Example:
            >>> api.delete("/users/1", status=204)
        """
        return self._exec(
            "DELETE", path, status, expected_json, keys, params, headers, None
        )

    def _exec(
        self,
        method: str,
        path: str,
        status: int,
        expected_json: dict | None,
        keys: list | None,
        params: dict | None,
        headers: dict | None,
        body: str | None,
    ) -> requests.Response | None:
        """
        Execute the HTTP request and validate the response.

        Internal method that makes the HTTP request and validates the response.

        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE).
            path: Request path.
            status: Expected status code.
            expected_json: Expected JSON response (optional).
            keys: Keys that must exist in response (optional).
            params: Query parameters (optional).
            headers: HTTP headers (optional).
            body: Request body (optional).

        Returns:
            requests.Response object if successful, None otherwise.
        """
        url = f"{self.url}{path}"
        start_time = time.perf_counter()

        try:
            method_func = getattr(requests, method.lower())
            kwargs = {"timeout": self.timeout}
            if params:
                kwargs["params"] = params
            if headers:
                kwargs["headers"] = headers
            if body:
                kwargs["data"] = body

            response = method_func(url, **kwargs)
            elapsed = (time.perf_counter() - start_time) * 1000

            passed = response.status_code == status
            if expected_json is not None:
                try:
                    passed = passed and response.json() == expected_json
                except Exception:
                    passed = False
            if keys:
                try:
                    resp_json = response.json()
                    passed = passed and all(k in resp_json for k in keys)
                except Exception:
                    passed = False

            self._print_result(passed, elapsed)
            return response
        except Exception as e:
            elapsed = (time.perf_counter() - start_time) * 1000
            self._print_result(False, elapsed)
            print(f"{RED}Error: {e}{RESET}")
            return None

    def _print_result(self, passed: bool, elapsed_ms: float) -> None:
        """
        Print the test result.

        Internal method that outputs the test result with colors.

        Args:
            passed: Whether the test passed.
            elapsed_ms: Execution time in milliseconds.
        """
        global _total_tests, _total_time
        self._counter += 1
        _total_tests += 1
        _total_time += elapsed_ms
        icon = "✅" if passed else "❌"
        color = GREEN if passed else RED
        print(
            f"{color}{BOLD}{icon} {self._counter}. {'PASSED' if passed else 'FAILED'}{RESET}"
        )


@atexit.register
def _print_summary() -> None:
    """Print test summary at program exit."""
    if _total_tests > 0:
        print(f"\ntime: {_total_time / 1000:.2f} s")