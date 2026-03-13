from rapidtest.ASGITestRunner import ASGITestRunner
from rapidtest.Utils import StatusCode
from rapidtest.data import data
from api import app  

test = ASGITestRunner(app)  

#LOGIN
test.post(path="/token", expected_status=StatusCode.OK_200, data={"username": "caja", "password": "caja"})

# GET
test.get(path="/", expected_status=StatusCode.OK_200, contain_keys=["message"])
test.get(path="/me", expected_status=StatusCode.OK_200, headers={"Authorization": "Bearer caja"})
test.get(path="/users", expected_status=StatusCode.OK_200, query_params={"email": "caja"})

#POST
test.post(path="/user", 
          expected_status=StatusCode.CREATED_201,
          json_data={"id":f"{data.generate_id()}" , "name": "test", "email": "test", "age":12, "password": "test"})

#PUT
test.put(path="/user/2734e76d-de18-4930-8531-54c39b3abe05", 
         expected_status=StatusCode.OK_200,
         json_data={"id":"2734e76d-de18-4930-8531-54c39b3abe05", "name": "updated", "email": "updated", "age":25, "password": "updated"})

#PATCH
test.patch(path="/user/2734e76d-de18-4930-8531-54c39b3abe05", 
           expected_status=StatusCode.OK_200,
           query_params={"age": 35})

#DELETE
test.delete(path="/user/2734e76d-de18-4930-8531-54c39b3abe05", 
            expected_status=StatusCode.ACCEPTED_202)