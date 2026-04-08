from rapidtest.performance import Performance

perf = Performance(
    base_url="http://localhost:8000",
    users=5,
    duration=3,
    timeout=10,
    delay=0.1,
)

perf.add_task(endpoint="/", method="GET")
perf.add_task(endpoint="/users", method="GET")
perf.add_task(
    endpoint="/token", method="POST", data={"username": "caja", "password": "caja"}
)

results = perf.run()

print("\n📋 Results dict:", results)
