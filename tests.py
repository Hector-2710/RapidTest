from rapidtest.RapidTest import Test
from rapidtest.RapidData import data
from rapidtest.Performance import Performance

fastTest = Test(url="http://127.0.0.1:8000")

user = data.generate_user(id=True, name=True, email=True, age=True, password=True, username=True)

fastTest.get(endpoint="/", expected_status=200)
fastTest.get(endpoint="/me", expected_status=200, headers={"Authorization": f"Bearer {user['email']}"})
fastTest.get(endpoint="/users", expected_status=200, params={"use_email": user["email"]})
fastTest.get(endpoint=f"/users/{user['email']}", expected_status=200)
fastTest.post(endpoint="/token", data={"username": "caja", "password": "caja"}, expected_status=200)
fastTest.post(endpoint="/user", json=user, expected_status=201)
fastTest.put(endpoint=f"/user/2734e76d-de18-4930-8531-54c39b3abe05", json=user, expected_status=200)
fastTest.patch(endpoint=f"/user/{user['id']}", params={"age": 35}, expected_status=200)
fastTest.delete(endpoint=f"/user/{user['id']}", expected_status=202)

performanceTest = Performance(
     base_url="http://127.0.0.1:8000", 
     users=1,           
     duration=10,    
     timeout=1      
)

performanceTest.add_get_task(endpoint="/")
performanceTest.run()
