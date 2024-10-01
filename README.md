# rate-limiting
This repository contains implementations of various rate limiting 
algorithms that are commonly used in software engineering.

Repository contains the following commonly used rate-limiting algorithms.
- [Leaky bucket](https://github.com/krispingal/rate-limiting/blob/main/src/rate_limiting/leaky_bucket.py)
- [Fixed window](https://github.com/krispingal/rate-limiting/blob/main/src/rate_limiting/fixed_window.py)
- [Sliding window counter](https://github.com/krispingal/rate-limiting/blob/main/src/rate_limiting/sliding_window_counter.py)
- [Sliding window log](https://github.com/krispingal/rate-limiting/blob/main/src/rate_limiting/sliding_window_log.py)
- [Token bucket](https://github.com/krispingal/rate-limiting/blob/main/src/rate_limiting/token_bucket.py)


## Usage
Install dependencies via `pip install .` or `pip install.[tests]`.
Run test cases by `python -m pytest`