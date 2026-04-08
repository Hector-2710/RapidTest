import asyncio
import json as _json
import time
import atexit
from urllib.parse import urlencode
from .utils import GREEN, RED, BOLD, RESET

_total_tests: int = 0
_total_time: float = 0.0


class ASGITest:
    __slots__ = ("app", "_loop", "_counter")

    def __init__(self, app) -> None:
        self.app = app
        self._loop = asyncio.new_event_loop()
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
        qs = urlencode(params).encode() if params else b""
        hdr_list = [
            (k.lower().encode(), v.encode()) for k, v in (headers or {}).items()
        ]
        return self._exec("GET", path, status, expected_json, keys, qs, hdr_list)

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
        path,
        status=204,
        expected_json=None,
        keys=None,
        params=None,
        headers=None,
        **_,
    ):
        qs = urlencode(params).encode() if params else b""
        hdr_list = [
            (k.lower().encode(), v.encode()) for k, v in (headers or {}).items()
        ]
        return self._exec("DELETE", path, status, expected_json, keys, qs, hdr_list)

    def _exec(self, method, path, status, expected_json, keys, qs, hdr_list, body=None):
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
        global _total_tests, _total_time
        self._counter += 1
        _total_tests += 1
        _total_time += end_time
        icon = "✅" if passed else "❌"
        color = GREEN if passed else RED
        print(
            f"{color}{BOLD}{icon} {self._counter}. {'PASSED' if passed else 'FAILED'}{RESET}"
        )

    async def _run(self, method, path, qs, hdr_list, body):
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
            nonlocal done
            if not done:
                done = True
                return {"type": "http.request", "body": rbody, "more_body": False}
            return {"type": "http.disconnect"}

        async def send(msg):
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
        self._loop.close()


@atexit.register
def _print_summary() -> None:
    if _total_tests > 0:
        print(f"\ntime: {_total_time / 1000:.2f} s")
