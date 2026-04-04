from rapidtest.test import Test
from rapidtest.data import Data
from rapidtest.status_code import StatusCode
from backend.main import app

test = Test(app=app, asgi_mode=True, simple_report=True)
new_email = Data.generate_email()

# LOGIN
response = test.post(
    path="/token",
    status=StatusCode.OK_200,
    data={"username": "caja", "password": "caja"},
)

# GET
test.get(path="/", status=StatusCode.OK_200, keys=["message"])
test.get(path="/me", status=StatusCode.OK_200, headers={"Authorization": "Bearer caja"})
test.get(path="/users", status=StatusCode.OK_200, params={"email": "caja"})

# #POST
test.post(
    path="/user",
    status=StatusCode.CREATED_201,
    json={
        "id": f"{Data.generate_id()}",
        "name": "test",
        "email": new_email,
        "age": 12,
        "password": "test",
    },
)

# PUT
test.put(
    path="/user/2734e76d-de18-4930-8531-54c39b3abe05",
    status=StatusCode.OK_200,
    json={
        "id": "2734e76d-de18-4930-8531-54c39b3abe05",
        "name": "updated",
        "email": "updated",
        "age": 25,
        "password": "updated",
    },
)

# PATCH
test.patch(
    path="/user/2734e76d-de18-4930-8531-54c39b3abe05",
    status=StatusCode.OK_200,
    params={"age": 35},
)

# DELETE
test.delete(
    path="/user/2734e76d-de18-4930-8531-54c39b3abe05", status=StatusCode.ACCEPTED_202
)
