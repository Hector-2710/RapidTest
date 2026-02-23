from requests import get
from faker import Faker
from utils import print_report

fake = Faker()

class FastTest:
    def __init__(self, url):
        self.url = url

    def get(self, endpoint: str, expected_status: int = 200, params: dict = None, headers: dict = None, **kwargs):
        full_url = f"{self.url}{endpoint}"
        
        try:
            response = get(full_url, params=params, headers=headers, **kwargs)
            status = response.status_code
            body = response.json()
            actual_url = response.url

            if status == expected_status:
                print_report("PASSED", actual_url, status, body)
            else:
                msg = f"Expected {expected_status}, but got {status}"
                print_report("FAILED", actual_url, status, body, error_msg=msg)
            
            return response

        except Exception as e:
            print(f"\n❌ CRITICAL ERROR connecting to {full_url}:")
            return None
   

    