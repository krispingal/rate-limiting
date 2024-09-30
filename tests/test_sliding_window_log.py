import pytest
import time
from unittest.mock import ANY
from src.rate_limiting.sliding_window_log import SlidingWindowLog


class TestSlidingWindowLog:
    def test_sliding_window_log(self):
        sliding_log = SlidingWindowLog(2, 2)
        assert sliding_log.allow_request(), "Should allow first request"
        time.sleep(1)
        assert sliding_log.allow_request(), "Should allow second request"
        assert not sliding_log.allow_request(), "Should not allow third request"
        time.sleep(1)
        assert sliding_log.allow_request(), "Should allow request after time has passed"
        assert (
            not sliding_log.allow_request()
        ), "Should not allow request until time has "

    @pytest.mark.xfail(raises=ValueError)
    @pytest.mark.parametrize("params", [(-2, 4), (5, -2)])
    def test_valid_params(self, params):
        SlidingWindowLog(*params)

    def test_sliding_window_log_state(self):
        sliding_log = SlidingWindowLog(4, 2)
        for i in range(4):
            sliding_log.allow_request()
        assert sliding_log.get_state() == {
            "capacity": 4,
            "window_size": 2,
            "log_summary": {"requests_count": 4, "oldest_request_timestamp": ANY},
        }, "Sliding window accepts all requests"

    @pytest.mark.parametrize("capacity, window_size", [(2, 3), (15, 1)])
    def test_sliding_window_log_rate_limit(self, capacity, window_size):
        sliding_log = SlidingWindowLog(capacity, window_size)
        assert sliding_log.get_rate_limit() == (capacity, window_size)
