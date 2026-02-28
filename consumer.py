from rapidtest.RapidTest import Test
from rapidtest.RapidData import Data

fastTest = Test(url="http://localhost:8000")

# # test 1
# fastTest.get("/", expected_status=200, expected_body={"Hello": "World"})

# # test 2
# id = Data.generate_id()
# fastTest.get(f"/post/{id}", expected_status=404, expected_body={"id": id})

# test 3
id = Data.generate_id()
fastTest.get("/post", expected_status=200, params={"id": id}, expected_body={"id": id})

# # test 4: POST
# user = Data.generate_auth_user()
# fastTest.post("/user", expected_status=201, data=user, expected_body=user)

# # test 5: PUT
# new_password = Data.generate_password()
# fastTest.put(f"/user/{user['username']}", data={"password": new_password}, expected_status=200)

# # test 6: DELETE
# fastTest.delete(f"/user/{user['username']}", expected_status=200)