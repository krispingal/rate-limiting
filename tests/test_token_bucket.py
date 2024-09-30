import time
from unittest.mock import ANY
from src.rate_limiting.token_bucket import TokenBucket


class TestTokenBucket:
    def test_initial_token_bucket_capacity(self):
        """Test that the token bucket starts with full capacity."""
        bucket = TokenBucket(5, 2)
        assert (
            bucket.allow_request()
        ), "Token bucket should allow request with full capacity"

    def test_request_reduction(self):
        bucket = TokenBucket(3, 2)  # Bucket with 3 tokens, refills 1 token/sec
        for i in range(3):
            assert bucket.allow_request(), f"Request {i+1} should be allowed"
        assert (
            not bucket.allow_request()
        ), "Request 4 should be denied due to lack of tokens"

    def test_token_refill(self):
        """Test that tokens are refilled correctly after some time."""
        bucket = TokenBucket(2, 1)  # 2 tokens capacity, refills 1 token/sec
        bucket.allow_request()
        bucket.allow_request()  # Consumed 2 tokens, bucket should be empty now
        assert not bucket.allow_request(), "No tokens should be left after two requests"
        time.sleep(1.1)  # Wait for tokens to be refilled
        assert bucket.allow_request(), "Token should be refilled after waiting"

    def test_token_state(self):
        """Test that state is correctly returned."""
        bucket = TokenBucket(2, 1)
        assert bucket.get_state() == {
            "capacity": 2,
            "rate": 1,
            "tokens": 2,
            "last checked": ANY,
        }
        bucket.allow_request()
        assert bucket.get_state() == {
            "capacity": 2,
            "rate": 1,
            "tokens": 1,
            "last checked": ANY,
        }, "State should reflect that tokens has reduced by 1 after consuming 1 token"

    def test_token_rate_limit(self):
        """Test that Token bucket rate limiter returns the correct rate limit."""
        bucket = TokenBucket(3, 4)
        assert bucket.get_rate_limit() == (
            3,
            1,
        ), "Should return the rate at which tokens get refilled."
