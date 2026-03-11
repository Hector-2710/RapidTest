import asyncio
import json
from typing import Any, Annotated
from collections.abc import Callable

class ASGITest:
    """
    Test class for ASGI applications

    This class allows you to make HTTP requests directly to an ASGI 
    application without needing to run a server.
    """

    def __init__(self, app: Annotated[Callable, "ASGI application"]):
        self.app = app
        self._captured_db_operations = []
        self._is_capturing = False

    def get(self, path: str, **kwargs) -> 'ASGIResponse':
        """Direct GET request via ASGI"""
        return self._sync_request("GET", path, **kwargs)
    
    def post(self, path: str, json_data: dict[str, Any] | None = None, **kwargs) -> 'ASGIResponse':
        """Direct POST request via ASGI"""
        body = kwargs.pop("body", None)
        headers = kwargs.pop("headers", {})
        
        if json_data:
            body = json.dumps(json_data).encode()
            headers["content-type"] = "application/json"
            
        return self._sync_request("POST", path, body=body, headers=headers, **kwargs)
    
    def put(self, path: str, json_data: dict[str, Any] | None = None, **kwargs) -> 'ASGIResponse':
        """Direct PUT request via ASGI"""
        body = kwargs.pop("body", None)
        headers = kwargs.pop("headers", {})
        
        if json_data:
            body = json.dumps(json_data).encode()
            headers["content-type"] = "application/json"
            
        return self._sync_request("PUT", path, body=body, headers=headers, **kwargs)
    
    def delete(self, path: str, **kwargs) -> 'ASGIResponse':
        """Direct DELETE request via ASGI"""
        return self._sync_request("DELETE", path, **kwargs)
    
    def patch(self, path: str, json_data: dict[str, Any] | None = None, **kwargs) -> 'ASGIResponse':
        """Direct PATCH request via ASGI"""
        body = kwargs.pop("body", None)
        headers = kwargs.pop("headers", {})
        
        if json_data:
            body = json.dumps(json_data).encode()
            headers["content-type"] = "application/json"
            
        return self._sync_request("PATCH", path, body=body, headers=headers, **kwargs)
    
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
            "query_string": self._encode_query_params(query_params or {}),
            "headers": self._encode_headers(headers or {}),
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
            "headers": dict(self._decode_headers(response_headers)),
            "content": response_content,
            "json": self._try_parse_json(response_content),
        }
    
    def _encode_query_params(self, params: dict[str, str]) -> bytes:
        """Encodes query params for ASGI scope"""
        if not params:
            return b""
        return "&".join(f"{k}={v}" for k, v in params.items()).encode()
    
    def _encode_headers(self, headers: dict[str, str]) -> list[tuple[bytes, bytes]]:
        """Encodes headers for ASGI scope"""
        encoded = []
        for key, value in headers.items():
            encoded.append((key.lower().encode(), value.encode()))
        return encoded
    
    def _decode_headers(self, headers: list[tuple[bytes, bytes]]) -> list[tuple[str, str]]:
        """Decodes headers from ASGI"""
        return [(key.decode(), value.decode()) for key, value in headers]
    
    def _try_parse_json(self, content: bytes) -> dict[str, Any] | None:
        """Attempts to parse JSON from response"""
        try:
            return json.loads(content.decode())
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None
    
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