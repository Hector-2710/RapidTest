from typing import Union, Any
import requests

"""
Type definitions for the RapidTest library.

This module contains all custom type aliases used throughout
the library for better code readability and maintainability.
"""

type URL = str
type JsonDict = dict[str, Any]
type Headers = dict[str, str]
type QueryParams = dict[str, Any]
type JsonData = Union[dict[str, Any], list, str, int, float, bool]
type RawData = Union[str, bytes, dict[str, Any]]
type HttpMethod = str
type Endpoint = str
type Response = Union[requests.Response, None]
type Results = dict[str, Any]
type StatusCode = int

type Seconds = int


