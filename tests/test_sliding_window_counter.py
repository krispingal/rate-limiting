import pytest
import time
from unittest.mock import ANY
from src.rate_limiting.sliding_window_counter import SlidingWindowCounter


class TestSlidingWindowCounter:
    def test_sliding_window_counter(self):
        sliding_counter = SlidingWindowCounter(2, 2, 2)
        assert sliding_counter.allow_request(), "Should allow first request"
        time.sleep(1.3)
        assert sliding_counter.allow_request(), "Should allow second request"
        assert not sliding_counter.allow_request(), "Should not allow third request"
        time.sleep(1.3)
        assert (
            sliding_counter.allow_request()
        ), "Should allow request after time has passed"
        assert (
            not sliding_counter.allow_request()
        ), "Should not allow request until time has passed"

    @pytest.mark.xfail(raises=ValueError)
    @pytest.mark.parametrize("params", [(-2, 4, 2), (5, -2, 2), (5, 2, -3)])
    def test_valid_params(self, params):
        SlidingWindowCounter(*params)

    def test_sliding_window_counter_state(self):
        sliding_counter = SlidingWindowCounter(4, 2, 2)
        for i in range(4):
            sliding_counter.allow_request()
        assert sliding_counter.get_state() == {
            "capacity": 4,
            "window_size": 2,
            "bucket_count": 2,
            "buckets": ANY,
            "total_requests_in_buckets": 4,
            "last_checked": ANY,
        }, "Sliding window accepts all requests"

    @pytest.mark.parametrize(
        "capacity, window_size, bucket_count", [(2, 3, 3), (15, 2, 2)]
    )
    def test_sliding_window_counter_rate_limit(
        self, capacity, window_size, bucket_count
    ):
        sliding_counter = SlidingWindowCounter(capacity, window_size, bucket_count)
        assert sliding_counter.get_rate_limit() == (capacity, window_size)
