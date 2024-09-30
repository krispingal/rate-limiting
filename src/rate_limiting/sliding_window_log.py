"""Implements sliding log rate limiting algorithm."""

import random
import time
from collections import deque
from src.rate_limiting.rate_limit_abc import RateLimiter


class SlidingWindowLog(RateLimiter):
    def __init__(self, capacity: int, window_size: int):
        if capacity <= 0 or window_size <= 0:
            raise ValueError("Capacity and window size must be positive integers")
        self._capacity = capacity
        self._window_size = window_size
        self._log = deque()

    def allow_request(self) -> bool:
        """
        Check if request can be allowed.

        Returns:
            bool: True if request should be allowed else False.

        """
        t = time.monotonic()
        # Remove/clean expired requests from log.
        while self._log and t - self._log[0] > self._window_size:
            self._log.popleft()
        # Check if capacity allows for this request
        if len(self._log) < self._capacity:
            self._log.append(t)
            return True
        return False

    def get_state(self) -> dict:
        """Returns state of the rate limiter."""
        return {
            "capacity": self._capacity,
            "window_size": self._window_size,
            "log_summary": {
                "requests_count": len(self._log),
                "oldest_request_timestamp": self._log[0] if self._log else None,
            },
        }

    def get_rate_limit(self) -> tuple[int, int]:
        return self._capacity, self._window_size


if __name__ == "__main__":
    rl = SlidingWindowLog(
        3, 2
    )  # Sliding window with capacity of 5 requests in the span of 2 sec
    for i in range(20):
        if rl.allow_request():
            print(f"Packet {i} forwarded")
        else:
            print(f"Packet {i} dropped")
        time.sleep(random.random())
