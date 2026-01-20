import time
from dataclasses import dataclass, field
from threading import Lock

@dataclass
class Metrics:
    _lock: Lock = field(default_factory=Lock, init=False)

    requests_total: int = 0
    segment_requests_total: int = 0

    segment_latency_ms_last: float = 0.0
    segment_latency_ms_avg: float = 0.0

    def inc_requests(self) -> None:
        with self._lock:
            self.requests_total += 1

    def observe_segment_latency(self, ms: float) -> None:
        with self._lock:
            self.segment_requests_total += 1
            self.segment_latency_ms_last = ms
            # running average
            n = self.segment_requests_total
            self.segment_latency_ms_avg = ((self.segment_latency_ms_avg * (n - 1)) + ms) / n

    def snapshot(self) -> dict:
        with self._lock:
            return {
                "requests_total": self.requests_total,
                "segment_requests_total": self.segment_requests_total,
                "segment_latency_ms_last": round(self.segment_latency_ms_last, 3),
                "segment_latency_ms_avg": round(self.segment_latency_ms_avg, 3),
            }

metrics = Metrics()

class Timer:
    def __enter__(self):
        self._t0 = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.elapsed_ms = (time.perf_counter() - self._t0) * 1000.0