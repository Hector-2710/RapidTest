import requests
from typing import Any, Annotated
from rapidtest.Utils import print_report, show_connection_error
from rapidtest.types import Response

class Test:
    """
    Main class for performing REST API integration tests.
    
    This class allows making HTTP requests and automatically validating 
    status codes and response bodies.
    """

    def __init__(self, *,
        url: Annotated[str, "The base URL of the API (e.g., 'http://localhost:8000')"],
        global_headers: Annotated[dict[str, str] | None, "Global headers to be applied to all requests (optional)"] = {}
        ):
        """
        Initializes the test client.

        Args:
            url (str): The base URL of the API (e.g., 'http://localhost:8000').
            global_headers (dict[str, str] | None): Global headers to be applied to all requests. 
        """
        self.url = url.rstrip('/')
        self.global_headers = global_headers  

    def get(self, *, 
            endpoint: Annotated[str, "The API endpoint to call"],
            expected_status: Annotated[int, "The expected HTTP status code (default: 200)"] = 200, 
            expected_json: Annotated[dict[str, Any] | None, "The expected JSON in response"] = None,
            contain_keys: Annotated[list[str] | None, "A subset of JSON keys that should be contained in the response"] = None,
            params: Annotated[dict[str, Any] | None, "The query parameters for the request"] = None,
            headers: Annotated[dict[str, str] | None, "The headers for the request"] = None,
            **kwargs) -> Response:
        """
        Performs a GET request and validates status code and response body.

        Args:
            endpoint: The API endpoint to call 
            expected_status: The expected HTTP status code (default: 200)
            expected_json: The expected JSON response body for validation (optional)
            contain_keys: A subset of JSON keys that should be contained in the response
            params: Query parameters to append to the request URL
            headers: HTTP headers to include in the request
            **kwargs: Additional arguments passed to the underlying requests.get()

        Returns:
            Response: The complete HTTP response object.
        
        """
        return self._request("GET", endpoint, expected_status, expected_json, 
                           params=params, headers=headers,contain_keys=contain_keys, **kwargs)

    def post(self, *, 
             endpoint: Annotated[str, "The API endpoint to call"],
             expected_status: Annotated[int, "The expected HTTP status code (default: 201)"] = 201, 
             input_json: Annotated[dict[str, Any] | None, "JSON data to send in the request body"] = None,
             expected_json: Annotated[dict[str, Any] | None, "The expected JSON in response"] = None,
             contain_keys: Annotated[list[str] | None, "A subset of JSON keys that should be contained in the response"] = None,
             data: Annotated[str | bytes | dict[str, Any] | None, "Raw data to send in the request body (alternative to input_json)"] = None,
             params: Annotated[dict[str, Any] | None, "Query parameters to append to the request URL"] = None,
             headers: Annotated[dict[str, str] | None, "HTTP headers to include in the request"] = None,
             **kwargs) -> Response:
        """
        Performs a POST request and validates status code and response body.
        
        Args:
            endpoint: The API endpoint to call 
            expected_status: The expected HTTP status code (default: 201)
            input_json: JSON data to send in the request body
            expected_json: The expected JSON in response 
            contain_keys: A subset of JSON keys that should be contained in the response
            data: Raw data to send in the request body (alternative to input_json)
            params: Query parameters to append to the request URL
            headers: HTTP headers to include in the request
            **kwargs: Additional arguments passed to the underlying requests.post()
        
        Returns:
            Response: The complete HTTP response object.
        
        Note:
            Prints test results (PASSED/FAILED) with response details to console.
            Use either 'input_json' or 'data' parameter, not both.
        """
        return self._request("POST", endpoint, expected_status, expected_json, 
                           json=input_json, data=data, params=params, headers=headers, contain_keys=contain_keys, **kwargs)

    def put(self, *, 
            endpoint: Annotated[str, "The API endpoint to call"], 
            expected_status: Annotated[int, "The expected HTTP status code (default: 200)"] = 200, 
            input_json: Annotated[dict[str, Any] | None, "JSON data to send in the request body"] = None,
            expected_json: Annotated[dict[str, Any] | None, "The expected JSON in response"] = None,
            contain_keys: Annotated[list[str] | None, "A subset of JSON keys that should be contained in the response"] = None,
            data: Annotated[str | bytes | dict[str, Any] | None, "Raw data to send in the request body (alternative to input_json)"] = None,
            params: Annotated[dict[str, Any] | None, "Query parameters to append to the request URL"] = None,
            headers: Annotated[dict[str, str] | None, "HTTP headers to include in the request"] = None,
            **kwargs) -> Response:
        """
        Performs a PUT request and validates status code and response body.
        
        Args:
            endpoint: The API endpoint to call 
            expected_status: The expected HTTP status code (default: 200)
            input_json: JSON data to send in the request body
            expected_json: The expected JSON response body for validation (optional)
            contain_keys: A subset of JSON keys that should be contained in the response
            data: Raw data to send in the request body (alternative to input_json)
            params: Query parameters to append to the request URL
            headers: HTTP headers to include in the request
            **kwargs: Additional arguments passed to the underlying requests.put()
        
        Returns:
            Response: The complete HTTP response object.
        
        Note:
            Prints test results (PASSED/FAILED) with response details to console.
            Use either 'input_json' or 'data' parameter, not both.
        """
        return self._request("PUT", endpoint, expected_status, expected_json, 
                           json=input_json, data=data, params=params, headers=headers, contain_keys=contain_keys, **kwargs)

    def patch(self, *, 
              endpoint: Annotated[str, "The API endpoint to call"], 
              expected_status: Annotated[int, "The expected HTTP status code"] = 200, 
              input_json: Annotated[dict[str, Any] | None, "JSON data to send in the request body"] = None,
              expected_json: Annotated[dict[str, Any] | None, "The expected JSON in response"] = None,
              data: Annotated[str | bytes | dict[str, Any] | None, "Raw data to send in the request body (alternative to input_json)"] = None,
              contain_keys: Annotated[list[str] | None, "A subset of JSON keys that should be contained in the response"] = None,
              params: Annotated[dict[str, Any] | None, "Query parameters to append to the request URL"] = None,
              headers: Annotated[dict[str, str] | None, "HTTP headers to include in the request"] = None,
              **kwargs) -> Response:
        """
        Performs a PATCH request and validates status code and response body.
        
        Args:
            endpoint: The API endpoint to call
            expected_status: The expected HTTP status code
            input_json: JSON data to send in the request body
            expected_json: The expected JSON in response
            contain_keys: A subset of JSON keys that should be contained in the response
            data: Raw data to send in the request body (alternative to input_json)
            params: Query parameters to append to the request URL
            headers: HTTP headers to include in the request
        
        Returns:
            Response: The complete HTTP response object.
        """
        return self._request("PATCH", endpoint, expected_status, expected_json, 
                           json=input_json, data=data, params=params, headers=headers, contain_keys=contain_keys, **kwargs)

    def delete(self, *, 
               endpoint: Annotated[str, "The API endpoint to call"], 
               expected_status: Annotated[int, "The expected HTTP status code"] = 204, 
               input_json: Annotated[dict[str, Any] | None, "JSON data to send in the request body"] = None,
               expected_json: Annotated[dict[str, Any] | None, "The expected JSON in response"] = None,
               contain_keys: Annotated[list[str] | None, "A subset of JSON keys that should be contained in the response"] = None,
               data: Annotated[str | bytes | dict[str, Any] | None, "Raw data to send in the request body (alternative to input_json)"] = None,
               params: Annotated[dict[str, Any] | None, "Query parameters to append to the request URL"] = None,
               headers: Annotated[dict[str, str] | None, "HTTP headers to include in the request"] = None,
               **kwargs) -> Response:
        """
        Performs a DELETE request and validates status code and response body.
        
        Args:
            endpoint: The API endpoint to call
            expected_status: The expected HTTP status code
            expected_json: The expected JSON in response
            input_json: JSON data to send in the request body
            contain_keys: A subset of JSON keys that should be contained in the response
            data: Raw data to send in the request body (alternative to input_json)
            params: Query parameters to append to the request URL
            headers: HTTP headers to include in the request
        
        Returns:
            Response: The HTTP response object if successful.
        """
        return self._request("DELETE", endpoint, expected_status, expected_json, 
                           json=input_json, data=data, params=params, headers=headers, contain_keys=contain_keys, **kwargs)

    def set_global_headers(self, headers: Annotated[dict[str, str] | None, "Global headers to be applied to all requests"]) -> None:
        """
        Sets global headers that will be applied to all subsequent requests.
        
        Args:
            headers: Headers to be applied globally.
        
        Example:
            test.set_global_headers({"Authorization": "Bearer token123"})
        """
        if headers is None:
            self.global_headers = {}
        else:
            self.global_headers.update(headers)

    def clear_global_headers(self) -> None:
        """
        Clears all global headers.
        """
        self.global_headers = {}

    def _merge_headers(self, request_headers: dict[str, str] | None) -> dict[str, str] | None:
        """
        Merges global headers with request-specific headers.
        Request-specific headers take precedence over global headers.
        
        """
        if not self.global_headers and not request_headers:
            return None
            
        merged = self.global_headers.copy()
        if request_headers:
            merged.update(request_headers)  
            
        return merged if merged else None

    def _request(
        self, 
        method: str, 
        endpoint: str, 
        expected_status: int = 200, 
        expected_json: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        contain_keys: list[str] | None= None,
        data: str | bytes | dict[str, Any] | None  = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        **kwargs
    ) -> Response:
        """
        Internal method to make requests and validate results.
        """
        url = f"{self.url}/{endpoint.lstrip('/')}"
        method_func = getattr(requests,method.lower())
        
        request_kwargs = {}
        if json is not None:
            request_kwargs['json'] = json
        if data is not None:
            request_kwargs['data'] = data
        if params is not None:
            request_kwargs['params'] = params

        merged_headers = self._merge_headers(headers)
        if merged_headers is not None:
            request_kwargs['headers'] = merged_headers
        
        request_kwargs.update(kwargs)

        keys = True
        if contain_keys is not None:
            keys = self._validate_contain_keys(expected_json, contain_keys)

        try:
            response = method_func(url, **request_kwargs)
            status_ok = response.status_code == expected_status
            body_ok = True
            error_msg = None
            try:
                response_json = response.json()
            except Exception:
                response_json = {"raw_content": response.text}
            
        
            if expected_json is not None:
                if response_json != expected_json:
                    body_ok = False
                    if status_ok:
                        if keys:
                            error_msg = "The expected JSON is not the correct"
                        else:
                            error_msg = "The expected JSON is not the correct and keys are not correct"
                    else:
                        if keys:
                            error_msg = f"Expected status {expected_status}, but got {response.status_code} and the expected JSON is not the correct"
                        else:
                            error_msg = f"Expected status {expected_status}, but got {response.status_code} and the expected JSON is not the correct and keys are not correct"

            if not status_ok and not error_msg:
                if keys:
                    error_msg = f"Expected status {expected_status}, but got {response.status_code}"
                else:
                    error_msg = f"Expected status {expected_status}, but got {response.status_code} and keys are not correct"

            if status_ok and body_ok:
                if keys:
                    print_report("PASSED", response.url, response.status_code, response_json)
                else:
                    error_msg = "Keys are not correct"
                    print_report("PASSED", response.url, response.status_code, response_json, error_msg=error_msg)
            else:
                print_report("FAILED", response.url, response.status_code, response_json, error_msg=error_msg)

            return response
            
        except Exception as e:
            show_connection_error(url, e)
            return None

    def _validate_contain_keys(self, response_json: dict, contain_keys: list) -> bool:
        """
        Validates that the response JSON contains the expected subset of keys.

        Args:
            response_json: The actual JSON response from the API.
            contain_keys: The subset of JSON keys that should be contained in the response.

        Returns:
            bool: True if the response contains the expected keys, False otherwise.
        """
  
        for item in contain_keys:
            if item not in response_json:
                return False
        return True

    
    