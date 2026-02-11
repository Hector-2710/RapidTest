from requests import get,post,put,delete
from faker import Faker

fake = Faker()

class FastTest:
    def __init__(self, url):
        self.url = url

    def get(self, endpoint, response):
        data = get(f"{self.url}{endpoint}")
        print(data.json())

        if data.status_code == response:
            print(f"GET {endpoint} - PASSED")
        else:            
            print(f"GET {endpoint} - FAILED: Expected {response}, got {data.status_code}")

    def post(self, endpoint, payload, response):
        data = post(f"{self.url}{endpoint}", json=payload)
        print(data.json())

        if data.status_code == response:
            print(f"POST {endpoint} - PASSED")
        else:            
            print(f"POST {endpoint} - FAILED: Expected {response}, got {data.status_code}")

class FastData:
    def __init__(self):
        pass
    
    @staticmethod
    def generate_name():
        return fake.name()