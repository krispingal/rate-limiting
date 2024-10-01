"""Implements a leaky bucket rate limiter algorithm."""

import queue
import time
from threading import Thread
from src.rate_limiting.rate_limit_abc import RateLimiter


class LeakyBucket(RateLimiter):
    def __init__(self, bucket_size: int, outflow_rate: int, handler):
        if bucket_size <= 0 and outflow_rate <= 0:
            raise ValueError("Bucket size and outflow rate should be positive")
        self.bucket_size = bucket_size
        self.outflow_rate = outflow_rate
        self.queue = queue.Queue(maxsize=bucket_size)
        self._running = True
        self.handler = handler
        self.consumer_thread = Thread(target=self.consumer, daemon=True)
        self.consumer_thread.start()

    def allow_request(self, request) -> bool:
        try:
            self.queue.put(request, block=False)
            return True
        except queue.Full:
            return False

    def get_state(self) -> dict:
        return {
            "bucket_size": self.bucket_size,
            "outflow_rate": self.outflow_rate,
            "queue_length": self.queue.qsize(),
        }

    def get_rate_limit(self) -> int:
        return self.outflow_rate

    def consumer(self):
        while self._running:
            for _ in range(self.outflow_rate):
                try:
                    item = self.queue.get(block=False)
                    self.handler(item)
                    self.queue.task_done()
                except queue.Empty:
                    break
                except Exception as ex:
                    print(f"Handler failed processing request {item}: {ex}")
            time.sleep(1)

    def stop(self):
        """Gracefully stop the consumer thread."""
        self._running = False
        self.consumer_thread.join()


def forward(item):
    print(f"Forwarded {item}")


if __name__ == "__main__":
    bucket = LeakyBucket(5, 2, forward)
    for i in range(20):
        if bucket.allow_request(f"Request {i}"):
            print(f"Accepted Request {i}")
        else:
            print(f"Rejected Request {i}")
        time.sleep(0.5)  # Adding some delay between requests

    time.sleep(3)  # Let the consumer process some requests
    bucket.stop()  # Gracefully stop the consumer

