from FastTest import FastTest
from FastData import FastData

fastTest = FastTest("http://localhost:8000")

# test 1
# fastTest.get("/", expected_status=200, expected_body={"Hello": "World"})

# test 2
# id = FastData.generate_id()
# fastTest.get(f"/post/{id}", expected_status=200, response_data={"id": id})

# test 3
# id = FastData.generate_id()
# fastTest.get("/post", expected_status=200, params={"id": id}, response_data={"id": id})

# test 4: POST
user = FastData.generate_auth_user()
fastTest.post("/user", expected_status=201, data=user, expected_body=user)

# test 5: PUT
new_password = FastData.generate_password()
fastTest.put(f"/user/{user['username']}", data={"password": new_password}, expected_status=200)

# test 6: DELETE
fastTest.delete(f"/user/{user['username']}", expected_status=200)