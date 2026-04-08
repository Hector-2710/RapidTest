import requests
import time
import atexit
from urllib.parse import urlencode
from .utils import GREEN, RED, BOLD, RESET

_total_tests: int = 0
_total_time: float = 0.0


class HTTPTest:
    __slots__ = ("url", "timeout", "_counter")

    def __init__(self, url, timeout=30):
        self.url = url.rstrip("/")
        self.timeout = timeout
        self._counter = 0

    def get(
        self,
        path,
        status=200,
        expected_json=None,
        keys=None,
        params=None,
        headers=None,
        **_,
    ):
        return self._exec(
            "GET", path, status, expected_json, keys, params, headers, None
        )

    def post(
        self,
        path,
        status=201,
        json=None,
        expected_json=None,
        keys=None,
        data=None,
        params=None,
        headers=None,
        **_,
    ):
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
        path,
        status=200,
        json=None,
        expected_json=None,
        keys=None,
        data=None,
        params=None,
        headers=None,
        **_,
    ):
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
        path,
        status=200,
        json=None,
        expected_json=None,
        keys=None,
        data=None,
        params=None,
        headers=None,
        **_,
    ):
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
        path,
        status=204,
        expected_json=None,
        keys=None,
        params=None,
        headers=None,
        **_,
    ):
        return self._exec(
            "DELETE", path, status, expected_json, keys, params, headers, None
        )

    def _exec(self, method, path, status, expected_json, keys, params, headers, body):
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
    if _total_tests > 0:
        print(f"\ntime: {_total_time / 1000:.2f} s")
