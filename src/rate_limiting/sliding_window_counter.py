"""Implement a Sliding window counter rate limiter"""

import random
import time
from collections import defaultdict

from src.rate_limiting.rate_limit_abc import RateLimiter


class SlidingWindowCounter(RateLimiter):

    def __init__(self, capacity: int, window_size: int, bucket_count):
        """
        Initialize the Sliding window counter rate limiter.
        Args:
            capacity:
            window_size:
            bucket_count:
        """
        if capacity <= 0 or window_size <= 0 or bucket_count <= 0:
            raise ValueError(
                f"Capacity {capacity}, window size {window_size} and bucket count {bucket_count} must be positive integers"
            )
        self._capacity = capacity
        self._window_size = window_size
        self._bucket_count = bucket_count
        self._bucket_duration = window_size / bucket_count
        self._buckets = defaultdict(int)
        self._last_checked = time.monotonic()

    def _current_bucket(self) -> int:
        """Determine the current bucket based on the current time."""
        t = time.monotonic()
        return t // self._bucket_duration

    def _clean_old_buckets(self):
        """Remove capacity of buckets that are outside the sliding window."""
        current_time = time.monotonic()
        current_bucket_key = self._current_bucket()
        elapsed_buckets = (current_time - self._last_checked) // self._bucket_duration
        if elapsed_buckets > self._bucket_count:
            self._buckets.clear()
        else:
            for bucket in list(self._buckets.keys()):
                if bucket < current_bucket_key - self._bucket_count:
                    del self._buckets[bucket]
            self._last_checked = current_time

    def allow_request(self) -> bool:
        """
        Check if request can be allowed.

        Returns:
            bool: True if request should be allowed else False.

        """
        self._clean_old_buckets()
        total_requests = sum(self._buckets.values())
        if total_requests < self._capacity:
            current_bucket = self._current_bucket()
            self._buckets[current_bucket] += 1
            return True
        return False

    def get_state(self) -> dict:
        """ "Return the current state of the rate limiter."""
        return {
            "capacity": self._capacity,
            "window_size": self._window_size,
            "bucket_count": self._bucket_count,
            "buckets": dict(self._buckets),
            "total_requests_in_buckets": sum(self._buckets.values()),
            "last_checked": self._last_checked,
        }

    def get_rate_limit(self) -> tuple:
        """Returns the rate limit configuration."""
        return self._capacity, self._window_size


if __name__ == "__main__":
    rl = SlidingWindowCounter(
        5, 6, 3
    )  # Sliding window with capacity of 6 requests in the span of 5 secs, and each bucket of 1 sec
    for i in range(20):
        if rl.allow_request():
            print(f"Packet {i} forwarded")
        else:
            print(f"Packet {i} dropped")
        time.sleep(random.random() + 0.6)
