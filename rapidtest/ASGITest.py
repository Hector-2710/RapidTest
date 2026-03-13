import asyncio
import json
from urllib.parse import urlencode
from typing import Any
from collections.abc import Callable

from .Utils import (
    decode_headers,
    encode_headers,
    encode_query_params,
    print_report,
    show_connection_error,
    try_parse_json,
)
class ASGIResponse:
    """Wrapper for ASGI responses that mimics requests.Response"""
    
    def __init__(self, data: dict[str, Any]):
        self.status_code = data["status_code"]
        self.headers = data["headers"]
        self._content = data["content"]
        self._json = data["json"]
    
    def json(self) -> dict[str, Any] | None:
        """Returns parsed JSON from response"""
        return self._json
    
    @property
    def content(self) -> bytes:
        """Returns raw content from response"""
        return self._content
    
    @property
    def text(self) -> str:
        """Returns content as string"""
        return self._content.decode()
    
    def __repr__(self):
        return f"<ASGIResponse [{self.status_code}]>"

class ASGITest:
    """
    Test class for ASGI applications

    This class allows you to make HTTP requests directly to an ASGI 
    application without needing to run a server.
    """

    def __init__(self, app: Callable):
        self.app = app

    def get(
        self,
        path: str,
        expected_status: int = 200,
        expected_json: dict | None = None,
        contain_keys: list[str] | None = None,
        **kwargs,
    ) -> ASGIResponse:
        """Direct GET request via ASGI with integrated validation."""
        return self._validated_request(
            "GET",
            path,
            expected_status=expected_status,
            expected_json=expected_json,
            contain_keys=contain_keys,
            **kwargs,
        )
    
    def post(
        self,
        path: str,
        json_data: dict[str, Any] | None = None,
        expected_status: int = 201,
        expected_json: dict | None = None,
        contain_keys: list[str] | None = None,
        **kwargs,
    ) -> ASGIResponse:
        """Direct POST request via ASGI with integrated validation."""
        body, headers = self._prepare_body_and_headers(json_data, kwargs)
        return self._validated_request(
            "POST",
            path,
            expected_status=expected_status,
            expected_json=expected_json,
            contain_keys=contain_keys,
            body=body,
            headers=headers,
            **kwargs,
        )
    
    def put(
        self,
        path: str,
        json_data: dict[str, Any] | None = None,
        expected_status: int = 200,
        expected_json: dict | None = None,
        contain_keys: list[str] | None = None,
        **kwargs,
    ) -> ASGIResponse:
        """Direct PUT request via ASGI with integrated validation."""
        body, headers = self._prepare_body_and_headers(json_data, kwargs)
        return self._validated_request(
            "PUT",
            path,
            expected_status=expected_status,
            expected_json=expected_json,
            contain_keys=contain_keys,
            body=body,
            headers=headers,
            **kwargs,
        )
    
    def delete(
        self,
        path: str,
        expected_status: int = 204,
        expected_json: dict | None = None,
        contain_keys: list[str] | None = None,
        **kwargs,
    ) -> ASGIResponse:
        """Direct DELETE request via ASGI with integrated validation."""
        return self._validated_request(
            "DELETE",
            path,
            expected_status=expected_status,
            expected_json=expected_json,
            contain_keys=contain_keys,
            **kwargs,
        )
    
    def patch(
        self,
        path: str,
        json_data: dict[str, Any] | None = None,
        expected_status: int = 200,
        expected_json: dict | None = None,
        contain_keys: list[str] | None = None,
        **kwargs,
    ) -> ASGIResponse:
        """Direct PATCH request via ASGI with integrated validation."""
        body, headers = self._prepare_body_and_headers(json_data, kwargs)
        return self._validated_request(
            "PATCH",
            path,
            expected_status=expected_status,
            expected_json=expected_json,
            contain_keys=contain_keys,
            body=body,
            headers=headers,
            **kwargs,
        )

    def _validated_request(
        self,
        method: str,
        path: str,
        *,
        expected_status: int,
        expected_json: dict | None,
        contain_keys: list[str] | None,
        **kwargs,
    ) -> ASGIResponse:
        try:
            response = self._sync_request(method, path, **kwargs)
            self._process_response_validation(response, path, expected_status, expected_json, contain_keys)
            return response
        except Exception as exception:
            simulated_url = f"asgi://testserver{path}"
            show_connection_error(simulated_url, exception)
            raise

    def _prepare_body_and_headers(self, json_data: dict[str, Any] | None, kwargs: dict) -> tuple[bytes | None, dict[str, str]]:
        body = kwargs.pop("body", None)
        form_data = kwargs.pop("data", None)
        headers = kwargs.pop("headers", {})

        if json_data is not None:
            body = json.dumps(json_data).encode()
            headers["content-type"] = "application/json"
        elif form_data is not None:
            body = urlencode(form_data, doseq=True).encode()
            headers["content-type"] = "application/x-www-form-urlencoded"

        return body, headers
    
    def _sync_request(self, method: str, path: str, **kwargs) -> 'ASGIResponse':
        """Helper to run async ASGI request in sync context"""
        response_data = asyncio.run(self._make_asgi_request(method, path, **kwargs))
        return ASGIResponse(response_data)
    
    async def _make_asgi_request(
        self, 
        method: str, 
        path: str, 
        headers: dict[str, str] | None  = None,
        body: bytes | None = None,
        query_params: dict[str, str] | None = None
    ) -> dict[str, Any]:
        """Core logic to make ASGI request and capture response"""

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
        
        if self._is_capturing:
            scope["rapidtest_capturing"] = True
            
        await self.app(scope, receive, send)
        
        response_content = b"".join(response_body)
        
        return {
            "status_code": response_status,
            "headers": dict(decode_headers(response_headers)),
            "content": response_content,
            "json": try_parse_json(response_content),
        }

    def _validate_contain_keys(self, response_json: dict, contain_keys: list[str]) -> bool:
        if not response_json:
            return False
        for item in contain_keys:
            if item not in response_json:
                return False
        return True

    def _process_response_validation(
        self,
        response: "ASGIResponse",
        path: str,
        expected_status: int,
        expected_json: dict | None = None,
        contain_keys: list[str] | None = None,
    ):
        simulated_url = f"asgi://testserver{path}"

        keys = True
        if contain_keys is not None:
            try:
                response_json = response.json()
                keys = self._validate_contain_keys(response_json, contain_keys)
            except Exception:
                response_json = {"raw_content": response.text if hasattr(response, "text") else str(response.content)}
                keys = False

        try:
            response_json = response.json()
        except Exception:
            response_json = {"raw_content": response.text if hasattr(response, "text") else str(response.content)}

        status_ok = response.status_code == expected_status
        body_ok = True
        error_msg = None

        if expected_json is not None and response_json != expected_json:
            body_ok = False
            if status_ok:
                error_msg = "The expected JSON is not the correct" if keys else "The expected JSON is not the correct and keys are not correct"
            else:
                error_msg = (
                    f"Expected status {expected_status}, but got {response.status_code} and the expected JSON is not the correct"
                    if keys
                    else f"Expected status {expected_status}, but got {response.status_code} and the expected JSON is not the correct and keys are not correct"
                )

        if not status_ok and not error_msg:
            error_msg = (
                f"Expected status {expected_status}, but got {response.status_code}"
                if keys
                else f"Expected status {expected_status}, but got {response.status_code} and keys are not correct"
            )

        if status_ok and body_ok:
            if keys:
                print_report("PASSED", simulated_url, response.status_code, response_json)
            else:
                print_report("PASSED", simulated_url, response.status_code, response_json, error_msg="Keys are not correct")
        else:
            print_report("FAILED", simulated_url, response.status_code, response_json, error_msg=error_msg)

        return status_ok and body_ok and keys



