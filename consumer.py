from FastTest import FastTest
from FastData import FastData

fastTest = FastTest("http://localhost:8000")

print("test 1")
fastTest.get("/", expected_status=200, expected_body={"Hello": "World"})

print("test 2")
fastTest.get("/", expected_status=200, expected_body={"Hello": "Wrong"})

print("test 3")
fastTest.get("/", expected_status=404, expected_body={"Hello": "Wrong"})

# print("test 2")
# id = FastData.generate_id()
# fastTest.get(f"/post/{id}", expected_status=200, response_data={"id": id})

# print("test 3")
# id = FastData.generate_id()
# fastTest.get("/post", expected_status=200, params={"id": id}, response_data={"id": id})
