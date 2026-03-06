from typing import Union, Optional, Any
import requests

"""
Type definitions for the RapidTest library.

This module contains all custom type aliases used throughout
the library for better code readability and maintainability.
"""

# HTTP-related types
URL = str
JsonDict = dict[str, Any]
Headers = dict[str, str]
QueryParams = dict[str, Any]
JsonData = Union[dict[str, Any], list, str, int, float, bool]
RawData = Union[str, bytes, dict[str, Any]]
HttpMethod = str
StatusCode = int
Endpoint = str
Response = Union[requests.Response, None]
Results = dict[str, Any]

