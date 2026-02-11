from library import FastTest, FastData
from performance_tester import FastTestPerformance

fastTest = FastTest("http://localhost:8000")

#test status
fastTest.get("/", 200)
fastTest.post("/post", {"username": FastData.generate_name()}, 400)

#test performance
performance_tester = FastTestPerformance("http://localhost:8000")
performance_tester.run_performance_test(users=20, spawn_rate=5, run_time="1m", endpoints=["/", "/post"])