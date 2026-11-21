# Fill in every ___ so the function does what its docstring says.
# Check your work:  python -m pytest practice -k advanced_02_concurrency_resilience   (or run check() in the lesson)
# Stuck? Fail a check twice to unlock the hints.
# Reset this file:  git checkout -- practice/exercises/advanced_02_concurrency_resilience.py

"""Advanced practice 2 — asyncio, TaskGroups, timeouts, threads, retries, idempotency.

Graded by the challenges in lessons 05–09. Requires Python 3.11+ (TaskGroup, asyncio.timeout).
"""
from __future__ import annotations

import asyncio
import random
import threading
from collections.abc import Awaitable, Callable, Iterable


async def gather_in_order(values: Iterable, worker: Callable[[object], Awaitable]) -> list:
    """Run worker(value) concurrently in an asyncio.TaskGroup; return results in INPUT order."""
    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(worker(value)) for value in values]
    return ___


async def with_timeout(awaitable: Awaitable, seconds: float) -> tuple[str, object]:
    """Return ('ok', result) or ('timeout', None) using asyncio.timeout()."""
    try:
        async with asyncio.timeout(seconds):
            return ___
    except TimeoutError:
        return ___


async def run_bounded(values: Iterable, worker: Callable[[object], Awaitable], limit: int) -> tuple[list, int]:
    """Run all workers concurrently but at most `limit` at a time (asyncio.Semaphore).

    Return (results in input order, peak number of workers running at once).
    """
    semaphore = ___
    active = peak = 0

    async def guarded(value):
        nonlocal active, peak
        async with semaphore:
            active += 1
            peak = ___
            try:
                return ___
            finally:
                active -= 1

    results = ___
    return results, peak


async def pipeline(items: Iterable, transform: Callable[[object], object], maxsize: int = 2) -> list:
    """Producer/consumer through a bounded asyncio.Queue; a None sentinel stops the consumer.

    Return transform(item) for each item, in order.
    """
    queue: asyncio.Queue = asyncio.Queue(maxsize=maxsize)
    output: list = []

    async def producer():
        for item in ___:
            await queue.put(item)
        await queue.put(None)

    async def consumer():
        while ___:
            output.append(transform(item))

    async with asyncio.TaskGroup() as group:
        group.create_task(___)
        group.create_task(___)
    return output


async def run_blocking(func: Callable, *args):
    """Run a blocking function without blocking the event loop (asyncio.to_thread)."""
    return ___


class SafeCounter:
    """A counter that is safe to increment from many threads (threading.Lock)."""

    def __init__(self) -> None:
        self._value = 0
        self._lock = ___

    def increment(self) -> None:
        with ___:
            self._value += 1

    @property
    def value(self) -> int:
        return ___


class TransientError(Exception):
    """A failure worth retrying (timeouts, 503s...)."""


class PermanentError(Exception):
    """A failure that will not fix itself (bad input, 404...)."""


def retry(operation: Callable[[], object], attempts: int = 3, base_delay: float = 0.1,
          sleep: Callable[[float], None] = None) -> object:
    """Call operation(); on TransientError wait base_delay * 2**n and try again.

    PermanentError is re-raised immediately. After `attempts` failures re-raise the
    last TransientError. `sleep` is injected so tests never really wait.
    """
    import time
    sleep = sleep or time.sleep
    for attempt in ___:
        try:
            return ___
        except TransientError:
            if ___:
                raise
            sleep(base_delay * 2 ** attempt)
    raise ValueError("attempts must be at least 1")


def jittered_delays(attempts: int, base: float, seed: int) -> list[float]:
    """Full-jitter backoff: delay n is uniform in [0, base * 2**n]. Same seed -> same delays."""
    rng = random.Random(seed)
    return ___


class IdempotentPayments:
    """charge(key, amount) runs the side effect once per key; duplicates return the first result.

    Reusing a key with a DIFFERENT amount raises ValueError.
    """

    def __init__(self, charge_card: Callable[[float], str]):
        self._charge_card = ___
        self._results: dict[str, tuple[float, str]] = {}

    def charge(self, key: str, amount: float) -> str:
        if ___:
            previous_amount, receipt = self._results[key]
            if ___:
                raise ValueError("idempotency key reused with different parameters")
            return receipt
        receipt = self._charge_card(amount)
        self._results[key] = (amount, receipt)
        return receipt


async def first_result(coroutines: list) -> object:
    """Run coroutines concurrently; return the first result to finish and cancel the rest.

    Hint: asyncio.wait(..., return_when=asyncio.FIRST_COMPLETED).
    """
    tasks = ___
    try:
        done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        return ___
    finally:
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)


def map_threaded(func: Callable, items: list, workers: int = 4) -> list:
    """Apply func to items with a ThreadPoolExecutor; results in input order."""
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=workers) as pool:
        return ___


class TokenBucket:
    """Rate limiter: `capacity` tokens, refilled at `rate` tokens/second from an injected clock.

    allow() consumes a token and returns True, or returns False if none are available.
    The bucket starts full and never holds more than capacity.
    """

    def __init__(self, capacity: int, rate: float, clock: Callable[[], float]):
        self.capacity, self.rate, self.clock = capacity, rate, clock
        self._tokens = ___
        self._last = clock()

    def allow(self) -> bool:
        now = ___
        self._tokens = min(self.capacity, self._tokens + (now - self._last) * self.rate)
        self._last = now
        if ___:
            self._tokens -= 1
            return True
        return False


class CircuitOpen(Exception):
    """Raised instead of calling the operation while the breaker is open."""


class CircuitBreaker:
    """After `threshold` consecutive failures the breaker opens: calls raise CircuitOpen
    without running. After `reset_after` seconds (injected clock) one trial call is allowed;
    success closes the breaker, failure re-opens it. Success resets the failure count.

    state is 'closed', 'open' or 'half-open'.
    """

    def __init__(self, threshold: int, reset_after: float, clock: Callable[[], float]):
        self.threshold, self.reset_after, self.clock = ___
        self.failures = 0
        self._opened_at = None

    @property
    def state(self) -> str:
        if ___:
            return "closed"
        if ___:
            return "half-open"
        return "open"

    def call(self, operation: Callable[[], object]):
        if ___:
            raise CircuitOpen("circuit is open")
        try:
            result = ___
        except Exception:
            self.failures += 1
            if ___:
                self._opened_at = self.clock()
            raise
        self.failures = 0
        self._opened_at = None
        return result
