import pytest
import time
from unittest.mock import ANY
from src.rate_limiting.fixed_window import FixedWindow


class TestFixedWindow:

    def test_fixed_window(self):
        window = FixedWindow(2, 2)
        window.allow_request()
        assert window.allow_request(), "Should allow two requests"
        assert not window.allow_request(), "Should not allow third request"
        time.sleep(2)
        assert (
            window.allow_request()
        ), "Should allow requests after initial window has passed"

    def test_window_state(self):
        window = FixedWindow(4, 2)
        for i in range(4):
            window.allow_request()
        assert window.get_state() == {
            "capacity": 4,
            "window size": 2,
            "counter": 4,
            "window start": ANY,
        }

    @pytest.mark.xfail(raises=ValueError)
    @pytest.mark.parametrize("params", [(-2, 4), (5, -2)])
    def test_valid_params(self, params):
        FixedWindow(*params)

    @pytest.mark.parametrize("capacity, window_size", [(2, 3), (15, 1)])
    def test_fixed_window_rate_limit(self, capacity, window_size):
        fixed_window = FixedWindow(capacity, window_size)
        assert fixed_window.get_rate_limit() == (capacity, window_size)
