"""
ASGITest: Direct ASGI application testing.

Provides testing of ASGI applications (FastAPI, Starlette, etc.) without
requiring an HTTP server. Tests are executed directly at the ASGI level.

Example:
    >>> from fastapi import FastAPI
    >>> from rapidtest import ASGITest
    >>> app = FastAPI()
    >>> @app.get("/health")
    ... def health():
    ...     return {"status": "ok"}
    >>> api = ASGITest(app)
    >>> api.get("/health", status=200)
    ✅ 1. PASSED
    >>> api.close()
"""

import asyncio
import json as _json
import time
import atexit
from urllib.parse import urlencode
from .utils import GREEN, RED, BOLD, RESET

_total_tests: int = 0
_total_time: float = 0.0


class ASGITest:
    """
    Direct ASGI application tester.

    Tests ASGI applications directly without needing an HTTP server.
    Creates its own event loop internally and executes requests synchronously
    while the application runs asynchronously.

    Attributes:
        app: The ASGI application to test.
        _loop: Internal asyncio event loop.
        _counter: Counter for the number of tests run.

    Example:
        >>> app = FastAPI()
        >>> @app.get("/users/{user_id}")
        ... def get_user(user_id: int):
        ...     return {"id": user_id, "name": f"User {user_id}"}
        >>> api = ASGITest(app)
        >>> api.get("/users/1", expected_json={"id": 1, "name": "User 1"})
        ✅ 1. PASSED
        >>> api.close()
    """

    __slots__ = ("app", "_loop", "_counter")

    def __init__(self, app) -> None:
        """
        Initialize ASGITest with an ASGI application.

        Args:
            app: An ASGI application callable (e.g., FastAPI app, Starlette app).
                Must conform to the ASGI specification.

        Example:
            >>> api = ASGITest(my_fastapi_app)
        """
        self.app = app
        self._loop = asyncio.new_event_loop()
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
    ) -> None:
        """
        Perform a GET request to the ASGI application.

        Args:
            path: The URL path (e.g., "/users/1", "/health").
            status: Expected HTTP status code (default: 200).
            expected_json: Exact JSON response expected (optional).
            keys: List of keys that must exist in the response (optional).
            params: Query parameters as a dictionary (optional).
            headers: HTTP headers as a dictionary (optional).
            **_: Ignore additional keyword arguments.

        Example:
            >>> api.get("/health", status=200)
            >>> api.get("/users", params={"role": "admin"}, keys=["id", "name"])
        """
        qs = urlencode(params).encode() if params else b""
        hdr_list = [
            (k.lower().encode(), v.encode()) for k, v in (headers or {}).items()
        ]
        return self._exec("GET", path, status, expected_json, keys, qs, hdr_list)

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
    ) -> None:
        """
        Perform a POST request to the ASGI application.

        Args:
            path: The URL path (e.g., "/users", "/posts").
            status: Expected HTTP status code (default: 201).
            json: JSON body as a dictionary (optional).
            expected_json: Exact JSON response expected (optional).
            keys: List of keys that must exist in the response (optional).
            data: Form data as a dictionary (optional).
            params: Query parameters (optional).
            headers: HTTP headers (optional).
            **_: Ignore additional keyword arguments.

        Example:
            >>> api.post("/users", json={"name": "Alice", "email": "alice@example.com"})
            >>> api.post("/login", data={"username": "alice", "password": "secret"})
        """
        qs = urlencode(params).encode() if params else b""
        hdr_list = [
            (k.lower().encode(), v.encode()) for k, v in (headers or {}).items()
        ]
        if json is not None:
            body = _json.dumps(json).encode()
            hdr_list.append((b"content-type", b"application/json"))
        elif data is not None:
            body = urlencode(data, doseq=True).encode()
            hdr_list.append((b"content-type", b"application/x-www-form-urlencoded"))
        else:
            body = None
        return self._exec("POST", path, status, expected_json, keys, qs, hdr_list, body)

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
    ) -> None:
        """
        Perform a PUT request to the ASGI application.

        Args:
            path: The URL path (e.g., "/users/1").
            status: Expected HTTP status code (default: 200).
            json: JSON body as a dictionary (optional).
            expected_json: Exact JSON response expected (optional).
            keys: List of keys that must exist in the response (optional).
            data: Form data as a dictionary (optional).
            params: Query parameters (optional).
            headers: HTTP headers (optional).
            **_: Ignore additional keyword arguments.

        Example:
            >>> api.put("/users/1", json={"name": "Updated Name"})
        """
        qs = urlencode(params).encode() if params else b""
        hdr_list = [
            (k.lower().encode(), v.encode()) for k, v in (headers or {}).items()
        ]
        if json is not None:
            body = _json.dumps(json).encode()
            hdr_list.append((b"content-type", b"application/json"))
        elif data is not None:
            body = urlencode(data, doseq=True).encode()
            hdr_list.append((b"content-type", b"application/x-www-form-urlencoded"))
        else:
            body = None
        return self._exec("PUT", path, status, expected_json, keys, qs, hdr_list, body)

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
    ) -> None:
        """
        Perform a PATCH request to the ASGI application.

        Args:
            path: The URL path (e.g., "/users/1").
            status: Expected HTTP status code (default: 200).
            json: JSON body as a dictionary (optional).
            expected_json: Exact JSON response expected (optional).
            keys: List of keys that must exist in the response (optional).
            data: Form data as a dictionary (optional).
            params: Query parameters (optional).
            headers: HTTP headers (optional).
            **_: Ignore additional keyword arguments.

        Example:
            >>> api.patch("/users/1", json={"name": "Partially Updated"})
        """
        qs = urlencode(params).encode() if params else b""
        hdr_list = [
            (k.lower().encode(), v.encode()) for k, v in (headers or {}).items()
        ]
        if json is not None:
            body = _json.dumps(json).encode()
            hdr_list.append((b"content-type", b"application/json"))
        elif data is not None:
            body = urlencode(data, doseq=True).encode()
            hdr_list.append((b"content-type", b"application/x-www-form-urlencoded"))
        else:
            body = None
        return self._exec(
            "PATCH", path, status, expected_json, keys, qs, hdr_list, body
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
    ) -> None:
        """
        Perform a DELETE request to the ASGI application.

        Args:
            path: The URL path (e.g., "/users/1").
            status: Expected HTTP status code (default: 204).
            expected_json: Exact JSON response expected (optional).
            keys: List of keys that must exist in the response (optional).
            params: Query parameters (optional).
            headers: HTTP headers (optional).
            **_: Ignore additional keyword arguments.

        Example:
            >>> api.delete("/users/1", status=204)
        """
        qs = urlencode(params).encode() if params else b""
        hdr_list = [
            (k.lower().encode(), v.encode()) for k, v in (headers or {}).items()
        ]
        return self._exec("DELETE", path, status, expected_json, keys, qs, hdr_list)

    def _exec(
        self,
        method: str,
        path: str,
        status: int,
        expected_json: dict | None,
        keys: list | None,
        qs: bytes,
        hdr_list: list,
        body: bytes | None = None,
    ) -> None:
        """
        Execute the request and validate the response.

        Internal method that runs the ASGI request and validates the response.

        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE).
            path: Request path.
            status: Expected status code.
            expected_json: Expected JSON response (optional).
            keys: Keys that must exist in response (optional).
            qs: Encoded query string.
            hdr_list: List of header tuples.
            body: Request body bytes (optional).
        """
        start_time = time.perf_counter()
        resp_json, status_code, headers_bytes, content = self._loop.run_until_complete(
            self._run(method, path, qs, hdr_list, body)
        )
        end_time = (time.perf_counter() - start_time) * 1000

        passed = status_code == status
        if expected_json is not None:
            passed = passed and resp_json == expected_json
        if keys:
            passed = passed and all(k in (resp_json or {}) for k in keys)

        self._print_result(passed, end_time)

    def _print_result(self, passed: bool, end_time: float) -> None:
        """
        Print the test result.

        Internal method that outputs the test result with colors.

        Args:
            passed: Whether the test passed.
            end_time: Execution time in milliseconds.
        """
        global _total_tests, _total_time
        self._counter += 1
        _total_tests += 1
        _total_time += end_time
        icon = "✅" if passed else "❌"
        color = GREEN if passed else RED
        print(
            f"{color}{BOLD}{icon} {self._counter}. {'PASSED' if passed else 'FAILED'}{RESET}"
        )

    async def _run(
        self,
        method: str,
        path: str,
        qs: bytes,
        hdr_list: list,
        body: bytes | None,
    ) -> tuple:
        """
        Run the ASGI request.

        Internal async method that constructs the ASGI scope, handles the
        request/response cycle, and returns the parsed response.

        Args:
            method: HTTP method (GET, POST, etc.).
            path: Request path.
            qs: Encoded query string.
            hdr_list: List of header tuples.
            body: Request body bytes.

        Returns:
            Tuple of (resp_json, status_code, headers, content).
        """
        scope = {
            "type": "http",
            "server": ("testserver", 80),
            "client": ("testclient", 12345),
            "scheme": "http",
            "root_path": "",
            "http_version": "1.1",
            "method": method,
            "path": path,
            "query_string": qs,
            "headers": hdr_list,
        }

        rbody = body or b""
        sent_body = []
        sent_headers = []
        resp_status = 200
        done = False

        async def receive():
            """ASGI receive coroutine."""
            nonlocal done
            if not done:
                done = True
                return {"type": "http.request", "body": rbody, "more_body": False}
            return {"type": "http.disconnect"}

        async def send(msg):
            """ASGI send coroutine."""
            nonlocal resp_status, sent_headers, sent_body
            t = msg["type"]
            if t == "http.response.start":
                resp_status = msg["status"]
                sent_headers = msg.get("headers", [])
            elif t == "http.response.body":
                c = msg.get("body", b"")
                if c:
                    sent_body.append(c)

        await self.app(scope, receive, send)

        content = b"".join(sent_body)
        resp_json = None
        try:
            if content:
                resp_json = _json.loads(content.decode())
        except Exception:
            pass

        return resp_json, resp_status, sent_headers, content

    def close(self) -> None:
        """
        Close the internal event loop.

        Should be called when done testing to properly clean up resources.
        Not strictly required but recommended.

        Example:
            >>> api = ASGITest(app)
            >>> api.get("/health")
            >>> api.close()
        """
        self._loop.close()


@atexit.register
def _print_summary() -> None:
    """Print test summary at program exit."""
    if _total_tests > 0:
        print(f"\ntime: {_total_time / 1000:.2f} s")