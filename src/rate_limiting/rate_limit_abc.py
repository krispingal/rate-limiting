from abc import ABC, abstractmethod


class RateLimiter(ABC):
    @abstractmethod
    def allow_request(self, *args, **kwargs) -> bool:
        """
        Check if a request is allowed based on the rate-limiting algorithm.
        The implementation vary depending on the algorithm (e.g., tokens, requests, sliding window).

        Returns:
            bool: True if request is allowed, False otherwise.
        """
        pass

    @abstractmethod
    def get_state(self) -> dict:
        """
        Get current state of the rate limiter.

        Returns:
            dict: A dictionary representing the internal state of the rate limiter.
        """
        pass

    @abstractmethod
    def get_rate_limit(self) -> tuple:
        """ "
        Return the rate limit configuration such as the number of allowed requests/tokens and the time window.

        Returns:
            tuple: tuple that captures the number of requests allowed for time interval/window.
        """
        pass
