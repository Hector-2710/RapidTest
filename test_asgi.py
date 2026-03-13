from rapidtest.ASGITestRunner import ASGITestRunner
from rapidtest.Utils import StatusCode
from api import app  

test = ASGITestRunner(app)  

#LOGIN
test.post(path="/token", expected_status=StatusCode.OK_200, data={"username": "caja", "password": "caja"})

# GET
test.get(path="/", expected_status=StatusCode.OK_200, contain_keys=["message"])
test.get(path="/me", expected_status=StatusCode.OK_200, headers={"Authorization": "Bearer caja"})
