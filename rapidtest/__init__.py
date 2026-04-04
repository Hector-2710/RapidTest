"""
RapidTest: A library for simplifying REST API testing.

Includes traditional HTTP testing, ASGI-level testing and Performance testing.
"""

from .test import Test as Test
from .data import Data as Data
from .performance import Performance as Performance
from .status_code import StatusCode as StatusCode

