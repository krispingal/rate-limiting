import pytest
import time
from unittest.mock import ANY
from src.rate_limiting.leaky_bucket import LeakyBucket

# @pytest.fixture
def forward(item):
    print(f"Forwarded item {item}")


class TestLeakyBucket:
    def test_leaky_bucket_allow_request(self):
        leaky_bucket = LeakyBucket(bucket_size=3, outflow_rate=1, handler=forward)

        assert leaky_bucket.allow_request("Request 1"), "Should allow first request"
        assert leaky_bucket.allow_request("Request 2"), "Should allow second request"
        assert leaky_bucket.allow_request("Request 3"), "Should allow third request"

        assert not leaky_bucket.allow_request("Request 4"), "Should not allow fourth request, bucket is full"

        time.sleep(1.1)
        # After some time, the bucket should allow one more request
        assert leaky_bucket.allow_request("Request 5"), "Should allow a request after time has passed"

    @pytest.mark.xfail(raises=ValueError)
    @pytest.mark.parametrize("bucket_size, outflow_rate", [(-2, 4), (5, -2)])
    def test_valid_params(self, bucket_size, outflow_rate):
        bucket = LeakyBucket(bucket_size, outflow_rate, forward)
        bucket.stop()


    def test_leaky_bucket_state(self):
        bucket = LeakyBucket(4, 1, forward)
        for i in range(4):
            bucket.allow_request(f"Request {i}")
        assert bucket.get_state() == {
            "bucket_size": 4,
            "outflow_rate": 1,
            "queue_length": ANY
        }, "Leaky bucket accepts all requests"
        bucket.stop()

    @pytest.mark.parametrize(
        "bucket_size, outflow_rate", [(2, 3), (15, 2)]
    )
    def test_leaky_bucket_rate_limit(self, bucket_size, outflow_rate):
        bucket = LeakyBucket(bucket_size, outflow_rate, forward)
        assert bucket.get_rate_limit() == outflow_rate
        bucket.stop()