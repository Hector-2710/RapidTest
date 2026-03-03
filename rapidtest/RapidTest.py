import requests
from typing import Optional, Dict, Any, Annotated, Union
from rapidtest.Utils import print_report, show_connection_error

class Test:
    """
    Main class for performing REST API integration tests.
    
    This class allows making HTTP requests and automatically validating 
    status codes and response bodies.
    """

    def __init__(self, *,
        url: Annotated[str, "The base URL of the API (e.g., 'http://localhost:8000')"]):
        """
        Initializes the test client.

        Args:
            url (str): The base URL of the API (e.g., 'http://localhost:8000').
        """
        self.url = url.rstrip('/')

    def _request(
        self, 
        method: str, 
        endpoint: str, 
        expected_status: int = 200, 
        expected_json: Optional[Dict[str, Any]] = None,
        json: Optional[Union[Dict[str, Any], list, str, int, float, bool]] = None,
        data: Optional[Union[str, bytes, Dict[str, Any]]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Optional[requests.Response]:
        """
        Internal method to make requests and validate results.
        """
        url = f"{self.url}/{endpoint.lstrip('/')}"
        method_func = getattr(requests, method.lower())
        
        request_kwargs = {}
        if json is not None:
            request_kwargs['json'] = json
        if data is not None:
            request_kwargs['data'] = data
        if params is not None:
            request_kwargs['params'] = params
        if headers is not None:
            request_kwargs['headers'] = headers
        
        request_kwargs.update(kwargs)
        
        try:
            response = method_func(url, **request_kwargs)
            status_ok = response.status_code == expected_status
            body_ok = True
            error_msg = None
            
            response_json = None
            try:
                response_json = response.json()
            except Exception:
                response_json = {"raw_content": response.text}
            
        
            if expected_json is not None:
                if response_json != expected_json:
                    body_ok = False
                    if status_ok:
                        error_msg = "The expected JSON is not the correct"
                    else:
                        error_msg = f"Expected status {expected_status}, but got {response.status_code} and the expected JSON is not the correct"

            if not status_ok and not error_msg:
                error_msg = f"Expected status {expected_status}, but got {response.status_code}"

            if status_ok and body_ok:
                print_report("PASSED", response.url, response.status_code, response_json)
            else:
                print_report("FAILED", response.url, response.status_code, response_json, error_msg=error_msg)

            return response
            
        except Exception as e:
            show_connection_error(url, e)
            return None

    def get(self, *, 
            endpoint: Annotated[str, "The API endpoint to call"],
            expected_status: Annotated[int, "The expected HTTP status code"] = 200, 
            expected_json: Annotated[Optional[Dict[str, Any]], "The expected JSON in response"] = None,
            params: Annotated[Optional[Dict[str, Any]], "The query parameters for the request"] = None,
            headers: Annotated[Optional[Dict[str, str]], "The headers for the request"] = None,
            **kwargs) -> Optional[requests.Response]:
        """Performs a GET request and validates status code and response body."""
        return self._request("GET", endpoint, expected_status, expected_json, 
                           params=params, headers=headers, **kwargs)

    def post(self, *, 
             endpoint: Annotated[str, "The API endpoint to call"],
             expected_status: Annotated[int, "The expected HTTP status code"] = 201, 
             expected_json: Annotated[Optional[Dict[str, Any]], "The expected JSON in response"] = None,
             json: Annotated[Optional[Union[Dict[str, Any], list, str, int, float, bool]], "The JSON data for the request"] = None,
             data: Annotated[Optional[Union[str, bytes, Dict[str, Any]]], "The data for the request"] = None,
             params: Annotated[Optional[Dict[str, Any]], "The query parameters for the request"] = None,
             headers: Annotated[Optional[Dict[str, str]], "The headers for the request"] = None,
             **kwargs) -> Optional[requests.Response]:
        """Performs a POST request and validates status code and response body."""
        return self._request("POST", endpoint, expected_status, expected_json, 
                           json=json, data=data, params=params, headers=headers, **kwargs)

    def put(self, *, 
            endpoint: Annotated[str, "The API endpoint to call"], 
            expected_status: Annotated[int, "The expected HTTP status code"] = 200, 
            expected_json: Annotated[Optional[Dict[str, Any]], "The expected JSON in response"] = None,
            json: Annotated[Optional[Union[Dict[str, Any], list, str, int, float, bool]], "The JSON data for the request"] = None,
            data: Annotated[Optional[Union[str, bytes, Dict[str, Any]]], "The data for the request"] = None,
            params: Annotated[Optional[Dict[str, Any]], "The query parameters for the request"] = None,
            headers: Annotated[Optional[Dict[str, str]], "The headers for the request"] = None,
            **kwargs) -> Optional[requests.Response]:
        """Performs a PUT request and validates status code and response body."""
        return self._request("PUT", endpoint, expected_status, expected_json, 
                           json=json, data=data, params=params, headers=headers, **kwargs)

    def patch(self, *, 
              endpoint: Annotated[str, "The API endpoint to call"], 
              expected_status: Annotated[int, "The expected HTTP status code"] = 200, 
              expected_json: Annotated[Optional[Dict[str, Any]], "The expected JSON in response"] = None,
              json: Annotated[Optional[Union[Dict[str, Any], list, str, int, float, bool]], "The JSON data for the request"] = None,
              data: Annotated[Optional[Union[str, bytes, Dict[str, Any]]], "The data for the request"] = None,
              params: Annotated[Optional[Dict[str, Any]], "The query parameters for the request"] = None,
              headers: Annotated[Optional[Dict[str, str]], "The headers for the request"] = None,
              **kwargs) -> Optional[requests.Response]:
        """Performs a PATCH request and validates status code and response body."""
        return self._request("PATCH", endpoint, expected_status, expected_json, 
                           json=json, data=data, params=params, headers=headers, **kwargs)

    def delete(self, *, 
               endpoint: Annotated[str, "The API endpoint to call"], 
               expected_status: Annotated[int, "The expected HTTP status code"] = 204, 
               expected_json: Annotated[Optional[Dict[str, Any]], "The expected JSON in response"] = None,
               json: Annotated[Optional[Union[Dict[str, Any], list, str, int, float, bool]], "The JSON data for the request"] = None,
               data: Annotated[Optional[Union[str, bytes, Dict[str, Any]]], "The data for the request"] = None,
               params: Annotated[Optional[Dict[str, Any]], "The query parameters for the request"] = None,
               headers: Annotated[Optional[Dict[str, str]], "The headers for the request"] = None,
               **kwargs) -> Optional[requests.Response]:
        """Performs a DELETE request and validates status code and response body."""
        return self._request("DELETE", endpoint, expected_status, expected_json, 
                           json=json, data=data, params=params, headers=headers, **kwargs)


    