import time
import threading
import requests
from typing import Any, Annotated


class Performance:
    """
    Simple performance testing module.

    Provides basic load testing functionality.
    """

    def __init__(
        self,
        *,
        base_url: Annotated[str | None, "Base URL to test"] = None,
        users: Annotated[
            int, "Number of concurrent users to simulate (default: 10)"
        ] = 10,
        duration: Annotated[int, "Test duration in seconds (default: 10)"] = 10,
        timeout: Annotated[int, "Max request timeout in seconds (default: 10)"] = 10,
        delay: Annotated[
            float, "Delay between requests in seconds (default: 0.1)"
        ] = 0.1,
    ):
        """
        Initialize the performance test.

        Args:
            base_url (str | None): Base URL to test
            users (int): Number of concurrent users to simulate
            duration (int): Test duration in seconds
            timeout (int): Request timeout in seconds
            delay (float): Delay between requests
        """
        self.base_url = base_url.rstrip("/") if base_url else None
        self.users = users
        self.duration = duration
        self.timeout = timeout
        self.delay = delay
        self.tasks = []
        self.results = []
        self.lock = threading.Lock()

    def add_task(
        self,
        *,
        endpoint: Annotated[str, "URL endpoint to test"],
        method: Annotated[str, "HTTP method (GET, POST, PUT, PATCH, DELETE)"] = "GET",
        params: Annotated[dict | None, "Query parameters"] = None,
        headers: Annotated[dict | None, "HTTP headers"] = None,
        json: Annotated[dict | None, "JSON body for POST/PUT/PATCH"] = None,
        data: Annotated[dict | str | None, "Form data for POST"] = None,
    ):
        """Add a request task.

        Args:
            endpoint: URL endpoint to test
            method: HTTP method (GET, POST, PUT, PATCH, DELETE)
            params: Query parameters
            headers: HTTP headers
            json: JSON body for POST/PUT/PATCH
            data: Form data for POST
        """
        self.tasks.append(
            {
                "endpoint": endpoint,
                "method": method.upper(),
                "params": params,
                "headers": headers,
                "json": json,
                "data": data,
            }
        )

    def run(self) -> dict[str, Any]:
        """Run the performance test."""
        if not self.tasks:
            raise ValueError("No tasks defined. Use add_task() before running.")

        if not self.base_url:
            raise ValueError("base_url is required for performance tests")

        print("🚀 Starting performance test")
        print(f"📍 URL: {self.base_url}")
        print(f"📋 Tasks: {len(self.tasks)}")
        for i, task in enumerate(self.tasks):
            print(f"   {i + 1}. {task['method']} {task['endpoint']}")
        print(f"👥 Users: {self.users}")
        print(f"⏱️  Duration: {self.duration}s")
        print(f"⛔ Max timeout: {self.timeout}")
        print("-" * 50)

        self.results = []
        self.start_time = time.time()
        self.stop_test = False

        threads = []
        for i in range(self.users):
            thread = threading.Thread(target=self._worker, args=(i,))
            threads.append(thread)
            thread.start()

        time.sleep(self.duration)
        self.stop_test = True

        for thread in threads:
            thread.join()

        return self._calculate_results()

    def _worker(self, worker_id: int):
        """Worker thread that makes HTTP requests."""
        session = requests.Session()
        task_index = 0

        while not self.stop_test:
            task = self.tasks[task_index % len(self.tasks)]
            task_index += 1

            url = f"{self.base_url}{task['endpoint']}"
            method = task["method"]
            params = task.get("params")
            headers = task.get("headers")
            json_body = task.get("json")
            data_body = task.get("data")

            start_time = time.time()
            try:
                if method == "GET":
                    response = session.get(
                        url, params=params, headers=headers, timeout=self.timeout
                    )
                elif method == "POST":
                    response = session.post(
                        url,
                        params=params,
                        headers=headers,
                        json=json_body,
                        data=data_body,
                        timeout=self.timeout,
                    )
                elif method == "PUT":
                    response = session.put(
                        url,
                        params=params,
                        headers=headers,
                        json=json_body,
                        timeout=self.timeout,
                    )
                elif method == "PATCH":
                    response = session.patch(
                        url,
                        params=params,
                        headers=headers,
                        json=json_body,
                        timeout=self.timeout,
                    )
                elif method == "DELETE":
                    response = session.delete(
                        url, params=params, headers=headers, timeout=self.timeout
                    )
                else:
                    continue

                end_time = time.time()
                with self.lock:
                    self.results.append(
                        {
                            "worker_id": worker_id,
                            "method": method,
                            "endpoint": task["endpoint"],
                            "status_code": response.status_code,
                            "response_time": (end_time - start_time) * 1000,
                            "success": 200 <= response.status_code < 400,
                        }
                    )

            except Exception as e:
                end_time = time.time()
                with self.lock:
                    self.results.append(
                        {
                            "worker_id": worker_id,
                            "method": method,
                            "endpoint": task["endpoint"],
                            "status_code": 0,
                            "response_time": (end_time - start_time) * 1000,
                            "success": False,
                            "error": str(e),
                        }
                    )

            time.sleep(self.delay)

    def _calculate_results(self) -> dict[str, Any]:
        """Calculate and display test results."""
        if not self.results:
            print("❌ No results collected")
            return {}

        total_requests = len(self.results)
        successful_requests = sum(1 for r in self.results if r["success"])
        failed_requests = total_requests - successful_requests

        response_times = [r["response_time"] for r in self.results if r["success"]]

        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            min_response_time = min(response_times)
            max_response_time = max(response_times)
        else:
            avg_response_time = min_response_time = max_response_time = 0

        rps = total_requests / self.duration if self.duration > 0 else 0
        success_rate = (
            (successful_requests / total_requests * 100) if total_requests > 0 else 0
        )

        results = {
            "total_requests": total_requests,
            "successful_requests": successful_requests,
            "failed_requests": failed_requests,
            "success_rate": round(success_rate, 2),
            "avg_response_time": round(avg_response_time, 2),
            "min_response_time": round(min_response_time, 2),
            "max_response_time": round(max_response_time, 2),
            "requests_per_second": round(rps, 2),
            "duration": self.duration,
            "users": self.users,
        }

        print("\n" + "=" * 60)
        print("📊 PERFORMANCE TEST RESULTS")
        print("=" * 60)
        print(f"🎯 Total Requests:      {results['total_requests']}")
        print(f"✅ Successful:          {results['successful_requests']}")
        print(f"❌ Failed:              {results['failed_requests']}")
        print(f"📈 Success Rate:        {results['success_rate']}%")
        print(f"⚡ Requests/sec:        {results['requests_per_second']}")
        print(f"⏱️  Avg Response Time:   {results['avg_response_time']}ms")
        print(f"🐌 Min Response Time:   {results['min_response_time']}ms")
        print(f"🐇 Max Response Time:   {results['max_response_time']}ms")
        print(f"👥 Concurrent Users:    {results['users']}")
        print(f"⏰ Test Duration:       {results['duration']}s")
        print("=" * 60)

        if results["success_rate"] >= 95:
            print("🟢 Excellent performance!")
        elif results["success_rate"] >= 80:
            print("🟡 Good performance")
        else:
            print("🔴 Poor performance - check server")

        return results
