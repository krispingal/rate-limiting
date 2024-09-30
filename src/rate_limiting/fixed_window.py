import time
from src.rate_limiting.rate_limit_abc import RateLimiter


class FixedWindow(RateLimiter):
    def __init__(self, capacity: int, window_size: int):
        if capacity <= 0 or window_size <= 0:
            raise ValueError("Capacity and window_size must be positive integers")
        self._capacity = capacity
        self._window_size = window_size
        self._window_start_time = time.monotonic()
        self._counter = 0

    def allow_request(self) -> bool:
        """
        Check if request can be allowed.

        Returns:
            bool: True if request should be allowed else False.
        """
        if time.monotonic() - self._window_start_time > self._window_size:
            self._window_start_time = time.time()
            self._counter = 0
        if self._counter >= self._capacity:
            return False
        self._counter += 1
        return True

    def get_state(self) -> dict:
        """Returns the state of the rate limiter."""
        return {
            "capacity": self._capacity,
            "window size": self._window_size,
            "counter": self._counter,
            "window start": time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(self._window_start_time)
            ),
        }

    def get_rate_limit(self) -> tuple:
        """Returns the maximum number of requests"""
        return self._capacity, self._window_size


if __name__ == "__main__":
    window = FixedWindow(4, 2)
    for i in range(20):
        if window.allow_request():
            print(f"packet {i} forwarded")
        else:
            print(f"packet dropped")
        time.sleep(0.3)
