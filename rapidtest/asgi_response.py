from typing import Any


class ASGIResponse:
    """Wrapper for ASGI responses that mimics requests.Response.

    Provides a compatible interface with requests.Response for seamless
    switching between HTTP and ASGI testing modes.
    """

    def __init__(self, data: dict[str, Any]) -> None:
        self.status_code: int = data["status_code"]
        self.headers: dict[str, str] = dict(data["headers"])
        self._content: bytes = data["content"]
        self._json: dict[str, Any] | None = data.get("json")

    def json(self) -> dict[str, Any] | None:
        """Returns parsed JSON from response.

        Returns:
            Parsed JSON dictionary or None if no JSON was present.
        """
        return self._json

    @property
    def content(self) -> bytes:
        """Returns raw content from response as bytes."""
        return self._content

    @property
    def text(self) -> str:
        """Returns content decoded as UTF-8 string.

        Returns:
            Content as string. Empty string if decoding fails.
        """
        return self._content.decode("utf-8", errors="replace")

    def __repr__(self) -> str:
        return f"<ASGIResponse [{self.status_code}]>"
