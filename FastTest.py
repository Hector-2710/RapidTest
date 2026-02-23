from requests import get
from utils import print_report

class FastTest:
    def __init__(self, url: str):
        self.url = url

    def get(self, endpoint: str, expected_status: int = 200, params: dict = None, headers: dict = None, **kwargs):
        url = f"{self.url}{endpoint}"
        
        try:
            response = get(url, params=params, headers=headers, **kwargs)
            actual_url = response.url

            if response.status_code == expected_status:
                print_report("PASSED", actual_url, response.status_code, response.json())
            else:
                print_report("FAILED", actual_url, response.status_code, response.json(), error_msg=f"Expected {expected_status}, but got {response.status_code}")
            
            return response

        except Exception as e:
            print(f"\n❌ CRITICAL ERROR connecting to {url}:")
            return None
   

    