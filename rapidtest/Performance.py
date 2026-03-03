import time
import threading
import requests
from typing import Dict, Any, Annotated
import statistics


class Performance:
    """
    Simple performance testing module using requests and threading.
    
    Provides basic load testing functionality without external dependencies.
    """

    def __init__(self, *, 
                 base_url: Annotated[str, "Base URL to test"],
                 users: Annotated[int, "Number of concurrent users to simulate (default: 10)"] = 10,
                 duration: Annotated[int, "Test duration in seconds (default: 10)"] = 10,
                 timeout: Annotated[int, "Max request timeout in seconds (default: 10)"] = 10):
        """
        Initialize the performance test.

        Args:
            base_url (str): The base URL to test
            users (int): Number of concurrent users to simulate
            duration (int): Test duration in seconds
            timeout (int): Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.users = users
        self.duration = duration
        self.timeout = timeout
        self.results = []
        self.lock = threading.Lock()
        
    def add_get_task(self, *, endpoint: Annotated[str, "URL endpoint to test"]):
        """Add a GET request task."""
        self.endpoint = endpoint
        
    def run(self) -> Dict[str, Any]:
        """
        Run the performance test.
        
        Returns:
            Dict[str, Any]: Test results and statistics
        """
        if not hasattr(self, 'endpoint'):
            raise ValueError("No endpoint defined. Use add_get_task() before running.")
            
        print("🚀 Starting performance test")
        print(f"📍 URL: {self.base_url}{self.endpoint}")
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
            
        print("\nWait while it finishes...")
        time.sleep(self.duration)
        self.stop_test = True
        
        for thread in threads:
            thread.join()
            
        return self._calculate_results()
    
    def _worker(self, worker_id: Annotated[int, "Worker thread ID"]):
        """Worker thread that makes HTTP requests."""
        session = requests.Session()
        url = f"{self.base_url}{self.endpoint}"
        
        while not self.stop_test:
            start_time = time.time()
            try:
                response = session.get(url, timeout=self.timeout)
                end_time = time.time()
                
                with self.lock:
                    self.results.append({
                        'worker_id': worker_id,
                        'status_code': response.status_code,
                        'response_time': (end_time - start_time) * 1000,  
                        'success': 200 <= response.status_code < 400,
                    })
                    
            except Exception as e:
                end_time = time.time()
                
                with self.lock:
                    self.results.append({
                        'worker_id': worker_id,
                        'status_code': 0,
                        'response_time': (end_time - start_time) * 1000,
                        'success': False,
                        'error': str(e),
                    })
            
            time.sleep(0.1)
    
    def _calculate_results(self) -> Dict[str, Any]:
        """Calculate and display test results."""
        if not self.results:
            print("❌ No results collected")
            return {}
            
        total_requests = len(self.results)
        successful_requests = sum(1 for r in self.results if r['success'])
        failed_requests = total_requests - successful_requests
        
        response_times = [r['response_time'] for r in self.results if r['success']]
        
        if response_times:
            avg_response_time = statistics.mean(response_times)
            min_response_time = min(response_times)
            max_response_time = max(response_times)
        else:
            avg_response_time = min_response_time = max_response_time = 0
            
        rps = total_requests / self.duration if self.duration > 0 else 0
        success_rate = (successful_requests / total_requests * 100) if total_requests > 0 else 0
        
        results = {
            'total_requests': total_requests,
            'successful_requests': successful_requests,
            'failed_requests': failed_requests,
            'success_rate': round(success_rate, 2),
            'avg_response_time': round(avg_response_time, 2),
            'min_response_time': round(min_response_time, 2),
            'max_response_time': round(max_response_time, 2),
            'requests_per_second': round(rps, 2),
            'duration': self.duration,
            'users': self.users
        }
        
        print("\n" + "="*60)
        print("📊 PERFORMANCE TEST RESULTS")
        print("="*60)
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
        print("="*60)
        
        # # Status indicator
        # if results['success_rate'] >= 95:
        #     print("🟢 Excellent performance!")
        # elif results['success_rate'] >= 80:
        #     print("🟡 Good performance")
        # else:
        #     print("🔴 Poor performance - check server")
            
        return results