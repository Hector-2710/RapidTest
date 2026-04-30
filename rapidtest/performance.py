"""
Performance: Load testing module.

Provides basic load testing functionality using threading to simulate
concurrent users. Tests endpoints under load and reports performance metrics.

Example:
    >>> from rapidtest import Performance
    >>> perf = Performance(base_url="https://api.example.com", users=10, duration=5)
    >>> perf.add_task(endpoint="/health", method="GET")
    >>> perf.add_task(endpoint="/users", method="GET")
    >>> results = perf.run()
"""

import time
import threading
import requests
from typing import Any, Annotated


class Performance:
    """
    Simple performance testing module.

    Provides load testing by simulating multiple concurrent users making
    requests to specified endpoints. Uses threading to simulate concurrency.

    Attributes:
        base_url: Base URL of the server being tested.
        users: Number of concurrent users to simulate.
        duration: Test duration in seconds.
        timeout: Maximum request timeout in seconds.
        delay: Delay between requests in seconds.
        tasks: List of task definitions.
        results: List of test results.

    Example:
        >>> perf = Performance(base_url="https://api.example.com", users=10, duration=5)
        >>> perf.add_task(endpoint="/health", method="GET")
        >>> perf.add_task(endpoint="/users", method="GET")
        >>> results = perf.run()
        >>> print(f"RPS: {results['requests_per_second']}")
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
    ) -> None:
        """
        Initialize the performance test.

        Args:
            base_url: Base URL of the server to test (optional, can be set later).
            users: Number of concurrent users to simulate (default: 10).
            duration: Test duration in seconds (default: 10).
            timeout: Maximum request timeout in seconds (default: 10).
            delay: Delay between requests in seconds (default: 0.1).

        Example:
            >>> perf = Performance(base_url="https://api.example.com", users=20, duration=30)
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
    ) -> None:
        """
        Add a request task to the performance test.

        Tasks are executed in rotation by each worker thread.

        Args:
            endpoint: URL endpoint to test (e.g., "/users", "/health").
            method: HTTP method (GET, POST, PUT, PATCH, DELETE). Default: GET.
            params: Query parameters as a dictionary (optional).
            headers: HTTP headers as a dictionary (optional).
            json: JSON body for POST/PUT/PATCH requests (optional).
            data: Form data for POST requests (optional).

        Example:
            >>> perf.add_task(endpoint="/health", method="GET")
            >>> perf.add_task(endpoint="/users", method="POST", json={"name": "Test"})
            >>> perf.add_task(endpoint="/users", method="GET", params={"limit": 10})
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
        """
        Run the performance test.

        Starts the specified number of worker threads, each making requests
        for the specified duration. Results are collected and statistics
        are calculated.

        Returns:
            Dictionary with performance metrics:
            - total_requests: Total number of requests executed.
            - successful_requests: Number of successful requests (2xx-3xx).
            - failed_requests: Number of failed requests.
            - success_rate: Success rate as a percentage.
            - avg_response_time: Average response time in milliseconds.
            - min_response_time: Minimum response time in milliseconds.
            - max_response_time: Maximum response time in milliseconds.
            - requests_per_second: Requests per second (RPS).
            - duration: Test duration in seconds.
            - users: Number of concurrent users.

        Raises:
            ValueError: If no tasks are defined or base_url is not set.

        Example:
            >>> perf = Performance(base_url="https://api.example.com", users=10, duration=5)
            >>> perf.add_task(endpoint="/health")
            >>> results = perf.run()
            >>> print(f"Success rate: {results['success_rate']}%")
            >>> print(f"RPS: {results['requests_per_second']}")
        """
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

    def _worker(self, worker_id: int) -> None:
        """
        Worker thread that makes HTTP requests.

        Internal method that runs in each worker thread, continuously
        making requests to the defined tasks until stop_test is True.

        Args:
            worker_id: Unique identifier for this worker thread.
        """
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
        """
        Calculate and display test results.

        Internal method that aggregates results and calculates statistics.

        Returns:
            Dictionary with performance metrics (same as run() return value).
        """
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