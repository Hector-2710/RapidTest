"""
RapidTest: A library for simplifying REST API testing.

Includes traditional HTTP testing, ASGI-level testing, and Performance testing.

Example:
    >>> from rapidtest import ASGITest
    >>> api = ASGITest(app)
    >>> api.get("/health", status=200)
    >>> api.close()
"""

from .asgi_test import ASGITest as ASGITest
from .data import Data as Data
from .http_test import HTTPTest as HTTPTest
from .performance import Performance as Performance
from .status_code import StatusCode as StatusCode