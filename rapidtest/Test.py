import requests
from typing import Any, Annotated
from rapidtest.Utils import show_connection_error, validate_and_report_response
from rapidtest.types import Response
from .ASGITest import ASGITest

class Test:
    """
    Main class for REST API integration tests.
    
    This class allows making HTTP requests and ASGI requests, validating
    responses, and printing detailed test reports to the console.
    """

    def __init__(
        self,
        *,
        url: Annotated[str | None, "The base URL of the API (e.g., 'http://localhost:8000')"] = None,
        app: Annotated[Any | None, "ASGI app instance when asgi=True"] = None,
        asgi_mode: Annotated[bool, "Enable ASGI direct testing mode"] = False,
        global_headers: Annotated[dict[str, str] | None, "Global headers to be applied to all requests (optional)"] = None,
    ):
        """
        Initializes the test client.

        Args:
            url (str | None): The base URL of the API (required when asgi=False).
            app (Any | None): ASGI app instance (required when asgi=True).
            asgi (bool | False): Enables ASGI mode for direct app testing without HTTP server.
            global_headers (dict[str, str] | None): Global headers to be applied to all requests.
        
        Note:
            - When asgi_mode=True, 'app' must be provided and 'url' is ignored
        """
        self.asgi_mode = asgi_mode
        self.url = (url or "").rstrip("/")
        self.global_headers = global_headers or {}
        self._asgi_runner: ASGITest | None = None

        if self.asgi_mode:
            if app is None:
                raise AttributeError(" atributte 'app' is required when asgi_mode=True")
            self._asgi_runner = ASGITest(app)
        elif not self.url:
            raise AttributeError(" atributte 'url' is required when asgi_mode=False")

    def get(self, *, 
            path: Annotated[str | None, "The API endpoint to call"] = None,
            status: Annotated[int, "The expected HTTP status code (default: 200)"] = 200, 
            json: Annotated[dict[str, Any] | None, "The expected JSON in response"] = None,
            keys: Annotated[list[str] | None, "A subset of JSON keys that should be contained in the response"] = None,
            params: Annotated[dict[str, Any] | None, "The query parameters for the request"] = None,
            headers: Annotated[dict[str, str] | None, "The headers for the request"] = None,
            **kwargs) -> Response:
        """
        Performs a GET request and validates status code and response body.

        Args:
            path: The API endpoint to call
            status: The expected HTTP status code (default: 200)
            json: The expected JSON response body for validation (optional)
            keys: A subset of JSON keys that should be contained in the response
            params: Query parameters to append to the request URL
            headers: HTTP headers to include in the request
            **kwargs: Additional arguments passed to the underlying requests.get()

        Returns:
            Response: The complete HTTP response object.
        
        """
        return self._request(method="GET", path=path, status=status, json=json, params=params, headers=headers, keys=keys, **kwargs)

    def post(self, *, 
             path: Annotated[str | None, "The API endpoint to call"] = None,
             status: Annotated[int, "The expected HTTP status code (default: 201)"] = 201, 
             json: Annotated[dict[str, Any] | None, "JSON data to send in the request body"] = None,
             expected_json: Annotated[dict[str, Any] | None, "The expected JSON in response"] = None,
             keys: Annotated[list[str] | None, "A subset of JSON keys that should be contained in the response"] = None,
             data: Annotated[str | bytes | dict[str, Any] | None, "Raw data to send in the request body (alternative to input_json)"] = None,
             params: Annotated[dict[str, Any] | None, "Query parameters to append to the request URL"] = None,
             headers: Annotated[dict[str, str] | None, "HTTP headers to include in the request"] = None,
             **kwargs) -> Response:
        """
        Performs a POST request and validates status code and response body.
        
        Args:
            path: The API endpoint to call 
            status: The expected HTTP status code (default: 201)
            json: JSON data to send in the request body
            expected_json: The expected JSON in response 
            keys: A subset of JSON keys that should be contained in the response
            data: Raw data to send in the request body (alternative to input_json)
            params: Query parameters to append to the request URL
            headers: HTTP headers to include in the request
            **kwargs: Additional arguments passed to the underlying requests.post()
        
        Returns:
            Response: The complete HTTP response object.
        
        Note:
            Prints test results (PASSED/FAILED) with response details to console.
            Use either 'json' or 'data' parameter, not both.
        """
        return self._request(method="POST", path=path, status=status, json=json,expected_json=expected_json, data=data, params=params, headers=headers, keys=keys, **kwargs)

    def put(self, *, 
            path: Annotated[str | None, "The API endpoint to call"] = None,
            status: Annotated[int, "The expected HTTP status code (default: 200)"] = 200, 
            json: Annotated[dict[str, Any] | None, "JSON data to send in the request body"] = None,
            expected_json: Annotated[dict[str, Any] | None, "The expected JSON in response"] = None,
            keys: Annotated[list[str] | None, "A subset of JSON keys that should be contained in the response"] = None,
            data: Annotated[str | bytes | dict[str, Any] | None, "Raw data to send in the request body (alternative to input_json)"] = None,
            params: Annotated[dict[str, Any] | None, "Query parameters to append to the request URL"] = None,
            headers: Annotated[dict[str, str] | None, "HTTP headers to include in the request"] = None,
            **kwargs) -> Response:
        """
        Performs a PUT request and validates status code and response body.
        
        Args:
            path: The API endpoint to call 
            status: The expected HTTP status code (default: 200)
            json: JSON data to send in the request body
            expected_json: The expected JSON response body for validation (optional)
            keys: A subset of JSON keys that should be contained in the response
            data: Raw data to send in the request body (alternative to json)
            params: Query parameters to append to the request URL
            headers: HTTP headers to include in the request
            **kwargs: Additional arguments passed to the underlying requests.put()
        
        Returns:
            Response: The complete HTTP response object.
        
        Note:
            Prints test results (PASSED/FAILED) with response details to console.
            Use either 'json' or 'data' parameter, not both.
        """
        return self._request(method="PUT", path=path, status=status, json=json, expected_json=expected_json, data=data, params=params, headers=headers, keys=keys, **kwargs)

    def patch(self, *, 
              path: Annotated[str | None, "The API endpoint to call"] = None,
              status: Annotated[int, "The expected HTTP status code"] = 200, 
              json: Annotated[dict[str, Any] | None, "JSON data to send in the request body"] = None,
              expected_json: Annotated[dict[str, Any] | None, "The expected JSON in response"] = None,
              data: Annotated[str | bytes | dict[str, Any] | None, "Raw data to send in the request body (alternative to json)"] = None,
              keys: Annotated[list[str] | None, "A subset of JSON keys that should be contained in the response"] = None,
              params: Annotated[dict[str, Any] | None, "Query parameters to append to the request URL"] = None,
              headers: Annotated[dict[str, str] | None, "HTTP headers to include in the request"] = None,
              **kwargs) -> Response:
        """
        Performs a PATCH request and validates status code and response body.
        
        Args:
            path: The API endpoint to call
            status: The expected HTTP status code
            json: JSON data to send in the request body
            expected_json: The expected JSON in response
            keys: A subset of JSON keys that should be contained in the response
            data: Raw data to send in the request body (alternative to json)
            params: Query parameters to append to the request URL
            headers: HTTP headers to include in the request
        
        Returns:
            Response: The complete HTTP response object.
        """
        return self._request(method="PATCH", path=path, status=status, json=json, expected_json=expected_json, data=data, params=params, headers=headers, keys=keys, **kwargs)

    def delete(self, *, 
               path: Annotated[str | None, "The API endpoint to call"] = None,
               status: Annotated[int, "The expected HTTP status code"] = 204, 
               json: Annotated[dict[str, Any] | None, "JSON data to send in the request body"] = None,
               expected_json: Annotated[dict[str, Any] | None, "The expected JSON in response"] = None,
               keys: Annotated[list[str] | None, "A subset of JSON keys that should be contained in the response"] = None,
               data: Annotated[str | bytes | dict[str, Any] | None, "Raw data to send in the request body (alternative to json)"] = None,
               params: Annotated[dict[str, Any] | None, "Query parameters to append to the request URL"] = None,
               headers: Annotated[dict[str, str] | None, "HTTP headers to include in the request"] = None,
               **kwargs) -> Response:
        """
        Performs a DELETE request and validates status code and response body.
        
        Args:
            path: The API endpoint to call
            status: The expected HTTP status code
            json: JSON data to send in the request body
            expected_json: The expected JSON in response
            keys: A subset of JSON keys that should be contained in the response
            data: Raw data to send in the request body (alternative to json)
            params: Query parameters to append to the request URL
            headers: HTTP headers to include in the request
        
        Returns:
            Response: The HTTP response object if successful.
        """
        return self._request(method="DELETE", path=path, status=status, json=json, expected_json=expected_json, data=data, params=params, headers=headers, keys=keys, **kwargs)

    def _request(
        self, *,
        method: str, 
        path: str, 
        status: int = 200, 
        json: dict[str, Any] | None = None,
        expected_json: dict[str, Any] | None = None,
        keys: list[str] | None= None,
        data: str | bytes | dict[str, Any] | None  = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        **kwargs
    ) -> Response:
        """
        Internal method to make requests and validate results.
        """
        merged_headers = self._merge_headers(headers)
        if self.asgi_mode:
            return self._asgi_request(
                method=method,
                path=path,
                status=status,
                expected_json=expected_json,
                json=json,
                keys=keys,
                data=data,
                params=params,
                headers=merged_headers,
                **kwargs,
            )

        return self._http_request(
            method=method,
            path=path,
            status=status,
            expected_json=expected_json,
            json=json,
            keys=keys,
            data=data,
            params=params,
            headers=merged_headers,
            **kwargs,
        )

    def _asgi_request(
        self,
        *,
        method: str,
        path: str,
        status: int,
        expected_json: dict[str, Any] | None,
        json: dict[str, Any] | None,
        keys: list[str] | None,
        data: str | bytes | dict[str, Any] | None,
        params: dict[str, Any] | None,
        headers: dict[str, str] | None,
        **kwargs,
    ):
        if not self._asgi_runner:
            raise RuntimeError("ASGI runner is not initialized")

        method_func = getattr(self._asgi_runner, method.lower())
        path = f"/{path.lstrip('/')}"

        request_kwargs = {}
        if json is not None:
            request_kwargs["json"] = json
        if data is not None:
            request_kwargs["data"] = data
        if params is not None:
            request_kwargs["query_params"] = params
        if headers is not None:
            request_kwargs["headers"] = headers

        request_kwargs.update(kwargs)

        return method_func(
            path=path,
            status=status,
            expected_json=expected_json,
            keys=keys,
            **request_kwargs,
        )

    def _http_request(
        self,
        *,
        method: str,
        path: str,
        status: int,
        expected_json: dict[str, Any] | None,
        json: dict[str, Any] | None,
        keys: list[str] | None,
        data: str | bytes | dict[str, Any] | None,
        params: dict[str, Any] | None,
        headers: dict[str, str] | None,
        **kwargs,
    ) -> Response:
        url = f"{self.url}/{path.lstrip('/')}"
        method_func = getattr(requests, method.lower())

        request_kwargs = {}
        if json is not None:
            request_kwargs["json"] = json
        if data is not None:
            request_kwargs["data"] = data
        if params is not None:
            request_kwargs["params"] = params
        if headers is not None:
            request_kwargs["headers"] = headers

        request_kwargs.update(kwargs)

        try:
            response = method_func(url, **request_kwargs)
            validate_and_report_response(
                response,
                response.url,
                status,
                expected_json,
                keys,
            )
            return response

        except Exception as e:
            show_connection_error(url, e)
            return None

    def set_global_headers(self, headers: dict[str, str] | None) -> None:
        """ Set Header for all requests."""
        if headers is None:
            self.global_headers = {}
        else:
            self.global_headers.update(headers)

    def clear_global_headers(self) -> None:
        """ Clears all global headers."""
        self.global_headers = {}

    def _merge_headers(self, request_headers: dict[str, str] | None) -> dict[str, str] | None:
        """ Merges global headers with request-specific headers."""
        if not self.global_headers and not request_headers:
            return None
            
        merged = self.global_headers.copy()
        if request_headers:
            merged.update(request_headers)  
            
        return merged if merged else None
    
    