from typing import Union, Any
import requests
import enum

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

class StatusCode(enum.IntEnum):
    CONTINUE = 100
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    MOVED_PERMANENTLY = 301
    TEMPORARY_REDIRECT = 307
    PERMANENT_REDIRECT = 308
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    NOT_ACCEPTABLE = 406
    REQUEST_TIMEOUT = 408
    INTERNAL_SERVER_ERROR = 500

