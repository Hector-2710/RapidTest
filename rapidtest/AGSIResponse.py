from typing import Any

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