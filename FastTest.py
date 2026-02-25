from requests import get, post
from utils import print_report



class FastTest:
    def __init__(self, url: str):
        self.url = url

    def get(self, endpoint: str, expected_status: int = 200, expected_body: dict = None, params: dict = None, headers: dict = None, **kwargs):
        url = f"{self.url}{endpoint}"
        
        try:
            response = get(url, params=params, headers=headers, **kwargs)
            status_ok = response.status_code == expected_status
            body_ok = True
            error_msg = None

            if expected_body is not None:
                if response.json() != expected_body:
                    body_ok = False
                    if status_ok:
                        error_msg = f"Body mismatch."
                    else:
                        error_msg = f"Expected status {expected_status}, but got {response.status_code} and body mismatch."

            if not status_ok and not error_msg:
                error_msg = f"Expected status {expected_status}, but got {response.status_code}"

            if status_ok and body_ok:
                print_report("PASSED", response.url, response.status_code, response.json())
            else:
                print_report("FAILED", response.url, response.status_code, response.json(), error_msg=error_msg)

            return response
            
        except Exception as e:
            print(f"\n❌ CRITICAL ERROR connecting to {url}: {str(e)}")
            return None

   
    def post(self, endpoint: str, expected_status: int = 200, expected_body: dict = None, data: dict = None, headers: dict = None, **kwargs):
        url = f"{self.url}{endpoint}"
        
        try:
            response = post(url, json=data, headers=headers, **kwargs)
            status_ok = response.status_code == expected_status
            body_ok = True
            error_msg = None

            if expected_body is not None:
                if response.json() != expected_body:
                    body_ok = False
                    if status_ok:
                        error_msg = f"Body mismatch."
                    else:
                        error_msg = f"Expected status {expected_status}, but got {response.status_code} and body mismatch."

            if not status_ok and not error_msg:
                error_msg = f"Expected status {expected_status}, but got {response.status_code}"

            if status_ok and body_ok:
                print_report("PASSED", response.url, response.status_code, response.json())
            else:
                print_report("FAILED", response.url, response.status_code, response.json(), error_msg=error_msg)

            return response
            
        except Exception as e:
            print(f"\n❌ CRITICAL ERROR connecting to {url}: {str(e)}")
            return None
    