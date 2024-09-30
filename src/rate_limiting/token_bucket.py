"""Implementation of Token Bucket rate limiting algorithm."""

import time
from src.rate_limiting.rate_limit_abc import RateLimiter


class TokenBucket(RateLimiter):
    def __init__(self, capacity: int, rate: int):
        """

        Args:
            capacity: Maximum number of tokens the bucket can hold at a time.
            rate: Rate (token per second) at which tokens are added.
        """
        if capacity <= 0 or rate <= 0:
            raise ValueError("Capacity and rate must be positive integers")
        self._capacity = capacity
        self._rate = rate
        self._tokens = capacity
        self._last_checked = time.time()

    def _add_tokens(self) -> None:
        """Adds token to bucket based on how much time elapsed after last check."""
        elapsed = time.time() - self._last_checked
        self._tokens = min(int(elapsed * self._rate) + self._tokens, self._capacity)
        self._last_checked = time.time()

    def allow_request(self, tokens_needed: int = 1) -> bool:
        """Check if request can be allowed.

        Args:
            tokens_needed: Number of tokens required for operation.

        Returns:
            bool: True if request should be allowed else False.
        """
        self._add_tokens()
        if self._tokens >= tokens_needed:
            self._tokens -= tokens_needed
            return True
        return False

    def get_state(self) -> dict:
        """Returns state of the rate limiter."""
        return {
            "capacity": self._capacity,
            "rate": self._rate,
            "tokens": self._tokens,
            "last checked": self._last_checked,
        }

    def get_rate_limit(self) -> tuple:
        """Returns the maximum tokens that can be consumed."""
        return self._capacity, 1


if __name__ == "__main__":
    rl = TokenBucket(5, 2)  # Bucket with capacity 5 tokens, rate of 2 tokens/sec
    for i in range(20):
        if rl.allow_request():
            print(f"Packet {i} forwarded")
        else:
            print(f"Packet {i} dropped")
        time.sleep(0.2)
