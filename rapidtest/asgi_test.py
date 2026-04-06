import asyncio
import json as json_lib
import time
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
        app: Annotated[Callable, "The ASGI application callable"],
        *,
        simple_report: Annotated[bool, "If True, only prints PASSED/FAILED"] = False,
    ):
        self.app = app
        self.simple_report = simple_report
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

    def get(
        self,
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
        path: Annotated[str | None, "The API endpoint to call"] = None,
        json: Annotated[
            dict[str, Any] | None, "JSON data to send in request body"
        ] = None,
        status: Annotated[int, "Expected HTTP status code"] = 201,
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
        path: Annotated[str | None, "The API endpoint to call"] = None,
        json: Annotated[
            dict[str, Any] | None, "JSON data to send in request body"
        ] = None,
        status: Annotated[int, "Expected HTTP status code"] = 200,
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
        path: Annotated[str | None, "The API endpoint to call"] = None,
        json: Annotated[
            dict[str, Any] | None, "JSON data to send in request body"
        ] = None,
        status: Annotated[int, "Expected HTTP status code"] = 200,
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
        method: Annotated[str, "HTTP method"],
        path: Annotated[str | None, "Request path"],
        status: Annotated[int, "Expected status code"],
        expected_json: Annotated[dict[str, Any] | None, "Expected JSON in response"],
        keys: Annotated[list[str] | None, "Keys to validate"],
        **kwargs,
    ) -> ASGIResponse:
        try:
            start_time = time.perf_counter()
            response = self._sync_request(method, path, **kwargs)
            elapsed = (time.perf_counter() - start_time) * 1000
            url = f"asgi://testserver{path}"
            validate_and_report_response(
                response,
                url,
                status,
                expected_json,
                keys,
                simple_report=self.simple_report,
                elapsed_ms=elapsed,
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
        response_data = self._loop.run_until_complete(
            self._make_asgi_request(method, path, **kwargs)
        )
        return ASGIResponse(response_data)

    def close(self) -> None:
        """Close the event loop."""
        self._loop.close()

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
        response_body: list[bytes] = []
        response_headers: list[tuple[bytes, bytes]] = []
        response_status = 200

        async def receive() -> dict[str, Any]:
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
