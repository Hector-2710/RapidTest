"""
RapidTest: A library for simplifying REST API testing.

Includes traditional HTTP testing and ASGI-level testing for maximum performance
and direct application testing without HTTP overhead.
"""

from .Test import Test as Test
from .data import data as data
from .Performance import Performance as Performance
from .Utils import StatusCode as StatusCode
from .ASGITestRunner import ASGITestRunner as ASGITestRunner



