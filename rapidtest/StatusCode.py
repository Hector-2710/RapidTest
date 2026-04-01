import enum


class StatusCode(enum.IntEnum):
    """HTTP status codes enum for API testing.

    Provides categorization methods and human-readable descriptions
    for all standard HTTP response codes.

    Example:
        >>> StatusCode.OK_200.is_success()
        True
        >>> StatusCode.NOT_FOUND_404.category
        'Client Error'
        >>> StatusCode.BAD_REQUEST_400.reason
        'Bad Request'
    """

    CONTINUE_100 = 100
    SWITCHING_PROTOCOLS_101 = 101
    PROCESSING_102 = 102
    OK_200 = 200
    CREATED_201 = 201
    ACCEPTED_202 = 202
    NON_AUTHORITATIVE_INFORMATION_203 = 203
    NO_CONTENT_204 = 204
    RESET_CONTENT_205 = 205
    PARTIAL_CONTENT_206 = 206
    MULTI_STATUS_207 = 207
    ALREADY_REPORTED_208 = 208
    IM_USED_226 = 226
    MULTIPLE_CHOICES_300 = 300
    MOVED_PERMANENTLY_301 = 301
    FOUND_302 = 302
    SEE_OTHER_303 = 303
    NOT_MODIFIED_304 = 304
    USE_PROXY_305 = 305
    TEMPORARY_REDIRECT_307 = 307
    PERMANENT_REDIRECT_308 = 308
    BAD_REQUEST_400 = 400
    UNAUTHORIZED_401 = 401
    PAYMENT_REQUIRED_402 = 402
    FORBIDDEN_403 = 403
    NOT_FOUND_404 = 404
    METHOD_NOT_ALLOWED_405 = 405
    NOT_ACCEPTABLE_406 = 406
    PROXY_AUTHENTICATION_REQUIRED_407 = 407
    REQUEST_TIMEOUT_408 = 408
    CONFLICT_409 = 409
    GONE_410 = 410
    LENGTH_REQUIRED_411 = 411
    PRECONDITION_FAILED_412 = 412
    PAYLOAD_TOO_LARGE_413 = 413
    URI_TOO_LONG_414 = 414
    UNSUPPORTED_MEDIA_TYPE_415 = 415
    RANGE_NOT_SATISFIABLE_416 = 416
    EXPECTATION_FAILED_417 = 417
    UNPROCESSABLE_ENTITY_422 = 422
    LOCKED_423 = 423
    FAILED_DEPENDENCY_424 = 424
    TOO_EARLY_425 = 425
    UPGRADE_REQUIRED_426 = 426
    PRECONDITION_REQUIRED_428 = 428
    TOO_MANY_REQUESTS_429 = 429
    REQUEST_HEADER_FIELDS_TOO_LARGE_431 = 431
    UNAVAILABLE_FOR_LEGAL_REASONS_451 = 451
    INTERNAL_SERVER_ERROR_500 = 500
    NOT_IMPLEMENTED_501 = 501
    BAD_GATEWAY_502 = 502
    SERVICE_UNAVAILABLE_503 = 503
    GATEWAY_TIMEOUT_504 = 504
    HTTP_VERSION_NOT_SUPPORTED_505 = 505
    VARIANT_ALSO_NEGOTIATES_506 = 506
    INSUFFICIENT_STORAGE_507 = 507
    LOOP_DETECTED_508 = 508
    NOT_EXTENDED_510 = 510
    NETWORK_AUTHENTICATION_REQUIRED_511 = 511

    @property
    def reason(self) -> str:
        """Returns the HTTP reason phrase for this status code.

        Returns:
            The standard HTTP reason phrase (e.g., 'OK', 'Not Found').
        """
        reasons = {
            100: "Continue",
            101: "Switching Protocols",
            102: "Processing",
            200: "OK",
            201: "Created",
            202: "Accepted",
            203: "Non-Authoritative Information",
            204: "No Content",
            205: "Reset Content",
            206: "Partial Content",
            207: "Multi-Status",
            208: "Already Reported",
            226: "IM Used",
            300: "Multiple Choices",
            301: "Moved Permanently",
            302: "Found",
            303: "See Other",
            304: "Not Modified",
            305: "Use Proxy",
            307: "Temporary Redirect",
            308: "Permanent Redirect",
            400: "Bad Request",
            401: "Unauthorized",
            402: "Payment Required",
            403: "Forbidden",
            404: "Not Found",
            405: "Method Not Allowed",
            406: "Not Acceptable",
            407: "Proxy Authentication Required",
            408: "Request Timeout",
            409: "Conflict",
            410: "Gone",
            411: "Length Required",
            412: "Precondition Failed",
            413: "Payload Too Large",
            414: "URI Too Long",
            415: "Unsupported Media Type",
            416: "Range Not Satisfiable",
            417: "Expectation Failed",
            422: "Unprocessable Entity",
            423: "Locked",
            424: "Failed Dependency",
            425: "Too Early",
            426: "Upgrade Required",
            428: "Precondition Required",
            429: "Too Many Requests",
            431: "Request Header Fields Too Large",
            451: "Unavailable For Legal Reasons",
            500: "Internal Server Error",
            501: "Not Implemented",
            502: "Bad Gateway",
            503: "Service Unavailable",
            504: "Gateway Timeout",
            505: "HTTP Version Not Supported",
            506: "Variant Also Negotiates",
            507: "Insufficient Storage",
            508: "Loop Detected",
            510: "Not Extended",
            511: "Network Authentication Required",
        }
        return reasons.get(self._value_, f"Unknown ({self._value_})")

    @property
    def category(self) -> str:
        """Returns the category name for this status code.

        Returns:
            One of: 'Informational', 'Success', 'Redirection',
                    'Client Error', 'Server Error'.
        """
        if 100 <= self._value_ < 200:
            return "Informational"
        elif 200 <= self._value_ < 300:
            return "Success"
        elif 300 <= self._value_ < 400:
            return "Redirection"
        elif 400 <= self._value_ < 500:
            return "Client Error"
        elif 500 <= self._value_ < 600:
            return "Server Error"
        return "Unknown"

    def is_informational(self) -> bool:
        """Check if status code is 1xx (Informational).

        Returns:
            True if status is in range 100-199.
        """
        return 100 <= self._value_ < 200

    def is_success(self) -> bool:
        """Check if status code is 2xx (Success).

        Returns:
            True if status is in range 200-299.
        """
        return 200 <= self._value_ < 300

    def is_redirect(self) -> bool:
        """Check if status code is 3xx (Redirection).

        Returns:
            True if status is in range 300-399.
        """
        return 300 <= self._value_ < 400

    def is_client_error(self) -> bool:
        """Check if status code is 4xx (Client Error).

        Returns:
            True if status is in range 400-499.
        """
        return 400 <= self._value_ < 500

    def is_server_error(self) -> bool:
        """Check if status code is 5xx (Server Error).

        Returns:
            True if status is in range 500-599.
        """
        return 500 <= self._value_ < 600

    def is_error(self) -> bool:
        """Check if status code is 4xx or 5xx (any error).

        Returns:
            True if status is >= 400.
        """
        return self._value_ >= 400
