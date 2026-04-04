import asyncio
import json as json_lib
from urllib.parse import urlencode
from typing import Any, Annotated
from collections.abc import Callable
from .asgi_response import ASGIResponse

from .utils import (
    decode_headers,
    encode_headers,
    encode_query_params,
    show_connection_error,
    try_parse_json,
    validate_and_report_response,
)


class ASGITest:
    """
    Test class for ASGI applications.

    This class allows you to make HTTP requests directly to an ASGI
    application without needing to run a server.
    """

    def __init__(
        self,
        *,
        app: Annotated[Callable, "The ASGI application callable"],
        simple_report: Annotated[bool, "If True, only prints PASSED/FAILED"] = False,
    ):
        self.app = app
        self.simple_report = simple_report

    def get(
        self,
        *,
        path: Annotated[str | None, "The API endpoint to call"] = None,
        status: Annotated[int, "Expected HTTP status code"] = 200,
        expected_json: Annotated[
            dict[str, Any] | None, "Expected JSON response body"
        ] = None,
        keys: Annotated[
            list[str] | None, "JSON keys that should be in response"
        ] = None,
        **kwargs,
    ) -> ASGIResponse:
        """Direct GET request via ASGI with integrated validation."""
        return self._validated_request(
            method="GET",
            path=path,
            status=status,
            expected_json=expected_json,
            keys=keys,
            **kwargs,
        )

    def post(
        self,
        *,
        path: Annotated[str | None, "The API endpoint to call"] = None,
        status: Annotated[int, "Expected HTTP status code"] = 201,
        json: Annotated[
            dict[str, Any] | None, "JSON data to send in request body"
        ] = None,
        expected_json: Annotated[
            dict[str, Any] | None, "Expected JSON response body"
        ] = None,
        keys: Annotated[
            list[str] | None, "JSON keys that should be in response"
        ] = None,
        **kwargs,
    ) -> ASGIResponse:
        """Direct POST request via ASGI with integrated validation."""
        body, headers = self._prepare_body_and_headers(json, kwargs)
        return self._validated_request(
            method="POST",
            path=path,
            status=status,
            expected_json=expected_json,
            keys=keys,
            body=body,
            headers=headers,
            **kwargs,
        )

    def put(
        self,
        *,
        path: Annotated[str | None, "The API endpoint to call"] = None,
        status: Annotated[int, "Expected HTTP status code"] = 200,
        json: Annotated[
            dict[str, Any] | None, "JSON data to send in request body"
        ] = None,
        expected_json: Annotated[
            dict[str, Any] | None, "Expected JSON response body"
        ] = None,
        keys: Annotated[
            list[str] | None, "JSON keys that should be in response"
        ] = None,
        **kwargs,
    ) -> ASGIResponse:
        """Direct PUT request via ASGI with integrated validation."""
        body, headers = self._prepare_body_and_headers(json, kwargs)
        return self._validated_request(
            method="PUT",
            path=path,
            status=status,
            expected_json=expected_json,
            keys=keys,
            body=body,
            headers=headers,
            **kwargs,
        )

    def delete(
        self,
        *,
        path: Annotated[str | None, "The API endpoint to call"] = None,
        status: Annotated[int, "Expected HTTP status code"] = 204,
        expected_json: Annotated[
            dict[str, Any] | None, "Expected JSON response body"
        ] = None,
        keys: Annotated[
            list[str] | None, "JSON keys that should be in response"
        ] = None,
        **kwargs,
    ) -> ASGIResponse:
        """Direct DELETE request via ASGI with integrated validation."""
        return self._validated_request(
            method="DELETE",
            path=path,
            status=status,
            expected_json=expected_json,
            keys=keys,
            **kwargs,
        )

    def patch(
        self,
        *,
        path: Annotated[str | None, "The API endpoint to call"] = None,
        status: Annotated[int, "Expected HTTP status code"] = 200,
        json: Annotated[
            dict[str, Any] | None, "JSON data to send in request body"
        ] = None,
        expected_json: Annotated[
            dict[str, Any] | None, "Expected JSON response body"
        ] = None,
        keys: Annotated[
            list[str] | None, "JSON keys that should be in response"
        ] = None,
        **kwargs,
    ) -> ASGIResponse:
        """Direct PATCH request via ASGI with integrated validation."""
        body, headers = self._prepare_body_and_headers(json, kwargs)
        return self._validated_request(
            method="PATCH",
            path=path,
            status=status,
            expected_json=expected_json,
            keys=keys,
            body=body,
            headers=headers,
            **kwargs,
        )

    def _validated_request(
        self,
        *,
        method: Annotated[str, "HTTP method"],
        path: Annotated[str | None, "Request path"],
        status: Annotated[int, "Expected status code"],
        expected_json: Annotated[dict[str, Any] | None, "Expected JSON in response"],
        keys: Annotated[list[str] | None, "Keys to validate"],
        **kwargs,
    ) -> ASGIResponse:
        try:
            response = self._sync_request(method, path, **kwargs)
            url = f"asgi://testserver{path}"
            validate_and_report_response(
                response,
                url,
                status,
                expected_json,
                keys,
                simple_report=self.simple_report,
            )
            return response
        except Exception as exception:
            url = f"asgi://testserver{path}"
            show_connection_error(url, exception)
            raise

    def _prepare_body_and_headers(
        self,
        json: Annotated[dict[str, Any] | None, "JSON data to send"],
        kwargs: Annotated[dict, "Additional kwargs"],
    ) -> Annotated[tuple[bytes | None, dict[str, str]], "body and headers"]:
        body = kwargs.pop("body", None)
        form_data = kwargs.pop("data", None)
        headers = kwargs.pop("headers", {})

        if json is not None:
            body = json_lib.dumps(json).encode()
            headers["content-type"] = "application/json"
        elif form_data is not None:
            body = urlencode(form_data, doseq=True).encode()
            headers["content-type"] = "application/x-www-form-urlencoded"

        return body, headers

    def _sync_request(
        self,
        method: Annotated[str | None, "HTTP method"],
        path: Annotated[str | None, "Request path"],
        **kwargs,
    ) -> Annotated[ASGIResponse, "Response object"]:
        """Helper to run async ASGI request in sync context."""
        response_data = asyncio.run(self._make_asgi_request(method, path, **kwargs))
        return ASGIResponse(response_data)

    async def _make_asgi_request(
        self,
        method: Annotated[str | None, "HTTP method"],
        path: Annotated[str | None, "Request path"],
        headers: Annotated[dict[str, str] | None, "Request headers"] = None,
        body: Annotated[bytes | None, "Request body bytes"] = None,
        query_params: Annotated[dict[str, str] | None, "Query parameters"] = None,
    ) -> Annotated[dict[str, Any], "Response data dict"]:
        """Core logic to make ASGI request and capture response."""

        scope = {
            "type": "http",
            "method": method.upper(),
            "path": path,
            "query_string": encode_query_params(query_params or {}),
            "headers": encode_headers(headers or {}),
            "server": ("testserver", 80),
            "client": ("testclient", 12345),
            "scheme": "http",
            "root_path": "",
            "http_version": "1.1",
        }

        request_body = body or b""
        request_complete = False
        response_started = False
        response_body = []
        response_headers = []
        response_status = 200

        async def receive():
            nonlocal request_complete
            if not request_complete:
                request_complete = True
                return {
                    "type": "http.request",
                    "body": request_body,
                    "more_body": False,
                }
            return {"type": "http.disconnect"}

        async def send(message):
            nonlocal response_started, response_headers, response_status, response_body

            if message["type"] == "http.response.start":
                response_started = True
                response_status = message["status"]
                response_headers = message.get("headers", [])

            elif message["type"] == "http.response.body":
                body_chunk = message.get("body", b"")
                if body_chunk:
                    response_body.append(body_chunk)

        await self.app(scope, receive, send)

        response_content = b"".join(response_body)

        return {
            "status_code": response_status,
            "headers": dict(decode_headers(response_headers)),
            "content": response_content,
            "json": try_parse_json(response_content),
        }


from .utils import (
    decode_headers,
    encode_headers,
    encode_query_params,
    show_connection_error,
    try_parse_json,
    validate_and_report_response,
)


class ASGITest:
    """
    Test class for ASGI applications.

    This class allows making HTTP requests directly to an ASGI application
    without needing to run a server. Useful for testing FastAPI, Starlette,
    and other ASGI frameworks.
    """

    def __init__(
        self,
        app: Annotated[Callable, "The ASGI application callable"],
        *,
        simple_report: Annotated[
            bool, "If True, only prints PASSED/FAILED without details"
        ] = False,
        timeout: Annotated[
            int | None, "Request timeout in seconds (None = no timeout)"
        ] = None,
    ):
        if not callable(app):
            raise TypeError("'app' must be a callable ASGI application")
        self.app = app
        self.simple_report = simple_report
        self.timeout = timeout

    def get(
        self,
        *,
        path: Annotated[str | None, "The API endpoint to call"] = None,
        status: Annotated[int, "Expected HTTP status code"] = 200,
        expected_json: Annotated[
            dict[str, Any] | None, "Expected JSON response body"
        ] = None,
        keys: Annotated[
            list[str] | None, "JSON keys that should be in response"
        ] = None,
        params: Annotated[
            dict[str, Any] | None, "Query parameters for the request"
        ] = None,
        headers: Annotated[dict[str, str] | None, "HTTP headers to include"] = None,
        **kwargs,
    ) -> ASGIResponse:
        """Performs a GET request via ASGI with integrated validation."""
        return self._validated_request(
            method="GET",
            path=path,
            status=status,
            expected_json=expected_json,
            keys=keys,
            params=params,
            headers=headers,
            **kwargs,
        )

    def post(
        self,
        *,
        path: Annotated[str | None, "The API endpoint to call"] = None,
        status: Annotated[int, "Expected HTTP status code"] = 201,
        json: Annotated[
            dict[str, Any] | None, "JSON data to send in request body"
        ] = None,
        data: Annotated[str | bytes | None, "Raw data to send in request body"] = None,
        expected_json: Annotated[
            dict[str, Any] | None, "Expected JSON response body"
        ] = None,
        keys: Annotated[
            list[str] | None, "JSON keys that should be in response"
        ] = None,
        params: Annotated[
            dict[str, Any] | None, "Query parameters for the request"
        ] = None,
        headers: Annotated[dict[str, str] | None, "HTTP headers to include"] = None,
        **kwargs,
    ) -> ASGIResponse:
        """Performs a POST request via ASGI with integrated validation."""
        body, extra_headers = self._prepare_body_and_headers(json, data, kwargs)
        merged_headers = self._merge_headers(headers, extra_headers)
        return self._validated_request(
            method="POST",
            path=path,
            status=status,
            expected_json=expected_json,
            keys=keys,
            params=params,
            headers=merged_headers,
            body=body,
            **kwargs,
        )

    def put(
        self,
        *,
        path: Annotated[str | None, "The API endpoint to call"] = None,
        status: Annotated[int, "Expected HTTP status code"] = 200,
        json: Annotated[
            dict[str, Any] | None, "JSON data to send in request body"
        ] = None,
        data: Annotated[str | bytes | None, "Raw data to send in request body"] = None,
        expected_json: Annotated[
            dict[str, Any] | None, "Expected JSON response body"
        ] = None,
        keys: Annotated[
            list[str] | None, "JSON keys that should be in response"
        ] = None,
        params: Annotated[
            dict[str, Any] | None, "Query parameters for the request"
        ] = None,
        headers: Annotated[dict[str, str] | None, "HTTP headers to include"] = None,
        **kwargs,
    ) -> ASGIResponse:
        """Performs a PUT request via ASGI with integrated validation."""
        body, extra_headers = self._prepare_body_and_headers(json, data, kwargs)
        merged_headers = self._merge_headers(headers, extra_headers)
        return self._validated_request(
            method="PUT",
            path=path,
            status=status,
            expected_json=expected_json,
            keys=keys,
            params=params,
            headers=merged_headers,
            body=body,
            **kwargs,
        )

    def patch(
        self,
        *,
        path: Annotated[str | None, "The API endpoint to call"] = None,
        status: Annotated[int, "Expected HTTP status code"] = 200,
        json: Annotated[
            dict[str, Any] | None, "JSON data to send in request body"
        ] = None,
        data: Annotated[str | bytes | None, "Raw data to send in request body"] = None,
        expected_json: Annotated[
            dict[str, Any] | None, "Expected JSON response body"
        ] = None,
        keys: Annotated[
            list[str] | None, "JSON keys that should be in response"
        ] = None,
        params: Annotated[
            dict[str, Any] | None, "Query parameters for the request"
        ] = None,
        headers: Annotated[dict[str, str] | None, "HTTP headers to include"] = None,
        **kwargs,
    ) -> ASGIResponse:
        """Performs a PATCH request via ASGI with integrated validation."""
        body, extra_headers = self._prepare_body_and_headers(json, data, kwargs)
        merged_headers = self._merge_headers(headers, extra_headers)
        return self._validated_request(
            method="PATCH",
            path=path,
            status=status,
            expected_json=expected_json,
            keys=keys,
            params=params,
            headers=merged_headers,
            body=body,
            **kwargs,
        )

    def delete(
        self,
        *,
        path: Annotated[str | None, "The API endpoint to call"] = None,
        status: Annotated[int, "Expected HTTP status code"] = 204,
        expected_json: Annotated[
            dict[str, Any] | None, "Expected JSON response body"
        ] = None,
        keys: Annotated[
            list[str] | None, "JSON keys that should be in response"
        ] = None,
        params: Annotated[
            dict[str, Any] | None, "Query parameters for the request"
        ] = None,
        headers: Annotated[dict[str, str] | None, "HTTP headers to include"] = None,
        **kwargs,
    ) -> ASGIResponse:
        """Performs a DELETE request via ASGI with integrated validation."""
        return self._validated_request(
            method="DELETE",
            path=path,
            status=status,
            expected_json=expected_json,
            keys=keys,
            params=params,
            headers=headers,
            **kwargs,
        )

    def head(
        self,
        *,
        path: Annotated[str | None, "The API endpoint to call"] = None,
        status: Annotated[int, "Expected HTTP status code"] = 200,
        params: Annotated[
            dict[str, Any] | None, "Query parameters for the request"
        ] = None,
        headers: Annotated[dict[str, str] | None, "HTTP headers to include"] = None,
        **kwargs,
    ) -> ASGIResponse:
        """Performs a HEAD request via ASGI with integrated validation."""
        return self._validated_request(
            method="HEAD",
            path=path,
            status=status,
            params=params,
            headers=headers,
            **kwargs,
        )

    def options(
        self,
        *,
        path: Annotated[str | None, "The API endpoint to call"] = None,
        status: Annotated[int, "Expected HTTP status code"] = 200,
        params: Annotated[
            dict[str, Any] | None, "Query parameters for the request"
        ] = None,
        headers: Annotated[dict[str, str] | None, "HTTP headers to include"] = None,
        **kwargs,
    ) -> ASGIResponse:
        """Performs an OPTIONS request via ASGI with integrated validation."""
        return self._validated_request(
            method="OPTIONS",
            path=path,
            status=status,
            params=params,
            headers=headers,
            **kwargs,
        )

    def _validated_request(
        self,
        *,
        method: str,
        path: str | None,
        status: int | None,
        expected_json: dict[str, Any] | None,
        keys: list[str] | None,
        params: dict[str, Any] | None,
        headers: dict[str, str] | None,
        body: bytes | None,
        **kwargs,
    ) -> ASGIResponse:
        """
        Internal method to make validated ASGI requests.

        Args:
            method: HTTP method (GET, POST, etc.)
            path: Request path
            status: Expected status code
            expected_json: Expected JSON in response
            keys: Keys to validate in response
            params: Query parameters
            headers: Request headers
            body: Request body bytes
            **kwargs: Additional arguments

        Returns:
            ASGIResponse: The validated response
        """
        try:
            response = self._sync_request(method, path, body, params, headers, **kwargs)
            url = f"asgi://testserver{path}"
            validate_and_report_response(
                response,
                url,
                status,
                expected_json,
                keys,
                simple_report=self.simple_report,
            )
            return response
        except Exception as exception:
            url = f"asgi://testserver{path}"
            show_connection_error(url, exception)
            raise

    def _prepare_body_and_headers(
        self,
        json: dict[str, Any] | None,
        data: str | bytes | None,
        kwargs: dict,
    ) -> tuple[bytes | None, dict[str, str]]:
        """
        Prepares request body and content-type header.

        Args:
            json: JSON data to send
            data: Raw data to send
            kwargs: Additional keyword arguments

        Returns:
            Tuple of (body_bytes, extra_headers)
        """
        body = kwargs.pop("body", None)
        form_data = kwargs.pop("data", None)
        extra_headers = {}

        if json is not None:
            body = json_lib.dumps(json).encode()
            extra_headers["content-type"] = "application/json"
        elif data is not None:
            if isinstance(data, str):
                body = data.encode()
            else:
                body = data
            extra_headers["content-type"] = "application/octet-stream"
        elif form_data is not None:
            if isinstance(form_data, dict):
                body = urlencode(form_data, doseq=True).encode()
                extra_headers["content-type"] = "application/x-www-form-urlencoded"
            else:
                body = form_data.encode() if isinstance(form_data, str) else form_data

        return body, extra_headers

    def _merge_headers(
        self,
        headers: dict[str, str] | None,
        extra_headers: dict[str, str],
    ) -> dict[str, str] | None:
        """
        Merges request headers with auto-generated headers.

        Args:
            headers: User-provided headers
            extra_headers: Auto-generated headers (content-type)

        Returns:
            Merged headers dict or None
        """
        if not headers and not extra_headers:
            return None
        merged = extra_headers.copy()
        if headers:
            merged.update(headers)
        return merged

    def _sync_request(
        self,
        method: str | None,
        path: str | None,
        body: bytes | None,
        params: dict[str, Any] | None,
        headers: dict[str, str] | None,
        **kwargs,
    ) -> ASGIResponse:
        """
        Helper to run async ASGI request in sync context.

        Args:
            method: HTTP method
            path: Request path
            body: Request body
            params: Query parameters
            headers: Request headers
            **kwargs: Additional arguments

        Returns:
            ASGIResponse wrapped response data
        """
        coro = self._make_asgi_request(method, path, headers, body, params, **kwargs)
        if self.timeout is not None:
            coro = asyncio.wait_for(coro, timeout=self.timeout)
        response_data = asyncio.run(coro)
        return ASGIResponse(response_data)

    async def _make_asgi_request(
        self,
        method: str | None,
        path: str | None,
        headers: dict[str, str] | None,
        body: bytes | None,
        query_params: dict[str, Any] | None,
        **kwargs,
    ) -> dict[str, Any]:
        """
        Core logic to make ASGI request and capture response.

        Args:
            method: HTTP method
            path: Request path
            headers: Request headers
            body: Request body bytes
            query_params: Query parameters dict
            **kwargs: Additional scope items

        Returns:
            Dict with status_code, headers, content, and json
        """
        scope = {
            "type": "http",
            "method": method.upper() if method else "GET",
            "path": path or "/",
            "query_string": encode_query_params(query_params or {}),
            "headers": encode_headers(headers or {}),
            "server": (kwargs.pop("server", "testserver"), kwargs.pop("port", 80)),
            "client": (
                kwargs.pop("client", "testclient"),
                kwargs.pop("client_port", 12345),
            ),
            "scheme": kwargs.pop("scheme", "http"),
            "root_path": kwargs.pop("root_path", ""),
            "http_version": kwargs.pop("http_version", "1.1"),
        }
        scope.update(kwargs)

        request_body = body or b""
        request_complete = False
        response_started = False
        response_body: list[bytes] = []
        response_headers: list[tuple[bytes, bytes]] = []
        response_status = 200

        async def receive() -> dict[str, Any]:
            """ASGI receive callable."""
            nonlocal request_complete
            if not request_complete:
                request_complete = True
                return {
                    "type": "http.request",
                    "body": request_body,
                    "more_body": False,
                }
            return {"type": "http.disconnect"}

        async def send(message: dict[str, Any]) -> None:
            """ASGI send callable."""
            nonlocal response_started, response_headers, response_status, response_body

            if message["type"] == "http.response.start":
                response_started = True
                response_status = message["status"]
                response_headers = message.get("headers", [])

            elif message["type"] == "http.response.body":
                body_chunk = message.get("body", b"")
                if body_chunk:
                    response_body.append(body_chunk)

        await self.app(scope, receive, send)

        response_content = b"".join(response_body)

        return {
            "status_code": response_status,
            "headers": dict(decode_headers(response_headers)),
            "content": response_content,
            "json": try_parse_json(response_content),
        }
