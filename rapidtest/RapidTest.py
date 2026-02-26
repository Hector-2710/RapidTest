import requests
from rapidtest.Utils import print_report


class Test:
    def __init__(self, url: str):
        self.url = url.rstrip('/')

    def _request(self, method: str, endpoint: str, expected_status: int = 200, expected_body: dict = None, **kwargs):
        url = f"{self.url}/{endpoint.lstrip('/')}"
        method_func = getattr(requests, method.lower())
        
        try:
            response = method_func(url, **kwargs)
            status_ok = response.status_code == expected_status
            body_ok = True
            error_msg = None
            
            response_json = None
            try:
                response_json = response.json()
            except Exception:
                response_json = {"raw_content": response.text}

            if expected_body is not None:
                if response_json != expected_body:
                    body_ok = False
                    if status_ok:
                        error_msg = "Body mismatch."
                    else:
                        error_msg = f"Expected status {expected_status}, but got {response.status_code} and body mismatch."

            if not status_ok and not error_msg:
                error_msg = f"Expected status {expected_status}, but got {response.status_code}"

            if status_ok and body_ok:
                print_report("PASSED", response.url, response.status_code, response_json)
            else:
                print_report("FAILED", response.url, response.status_code, response_json, error_msg=error_msg)

            return response
            
        except Exception as e:
            print(f"\n❌ CRITICAL ERROR connecting to {url}: {str(e)}")
            return None

    def get(self, endpoint: str, expected_status: int = 200, expected_body: dict = None, **kwargs):
        return self._request("GET", endpoint, expected_status, expected_body, **kwargs)

    def post(self, endpoint: str, expected_status: int = 200, expected_body: dict = None, **kwargs):
        return self._request("POST", endpoint, expected_status, expected_body, **kwargs)

    def put(self, endpoint: str, expected_status: int = 200, expected_body: dict = None, **kwargs):
        return self._request("PUT", endpoint, expected_status, expected_body, **kwargs)

    def patch(self, endpoint: str, expected_status: int = 200, expected_body: dict = None, **kwargs):
        return self._request("PATCH", endpoint, expected_status, expected_body, **kwargs)

    def delete(self, endpoint: str, expected_status: int = 200, expected_body: dict = None, **kwargs):
        return self._request("DELETE", endpoint, expected_status, expected_body, **kwargs)

    