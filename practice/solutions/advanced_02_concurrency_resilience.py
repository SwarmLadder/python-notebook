"""Advanced practice 2 — asyncio, TaskGroups, timeouts, threads, retries, idempotency.

Companion to advanced/exercises/02_concurrency_resilience_exercises.ipynb and
lessons 05–09. Requires Python 3.11+ (TaskGroup, asyncio.timeout).
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
    return [task.result() for task in tasks]


async def with_timeout(awaitable: Awaitable, seconds: float) -> tuple[str, object]:
    """Return ('ok', result) or ('timeout', None) using asyncio.timeout()."""
    try:
        async with asyncio.timeout(seconds):
            return "ok", await awaitable
    except TimeoutError:
        return "timeout", None


async def run_bounded(values: Iterable, worker: Callable[[object], Awaitable], limit: int) -> tuple[list, int]:
    """Run all workers concurrently but at most `limit` at a time (asyncio.Semaphore).

    Return (results in input order, peak number of workers running at once).
    """
    semaphore = asyncio.Semaphore(limit)
    active = peak = 0

    async def guarded(value):
        nonlocal active, peak
        async with semaphore:
            active += 1
            peak = max(peak, active)
            try:
                return await worker(value)
            finally:
                active -= 1

    results = await gather_in_order(values, guarded)
    return results, peak


async def pipeline(items: Iterable, transform: Callable[[object], object], maxsize: int = 2) -> list:
    """Producer/consumer through a bounded asyncio.Queue; a None sentinel stops the consumer.

    Return transform(item) for each item, in order.
    """
    queue: asyncio.Queue = asyncio.Queue(maxsize=maxsize)
    output: list = []

    async def producer():
        for item in items:
            await queue.put(item)
        await queue.put(None)

    async def consumer():
        while (item := await queue.get()) is not None:
            output.append(transform(item))

    async with asyncio.TaskGroup() as group:
        group.create_task(producer())
        group.create_task(consumer())
    return output


async def run_blocking(func: Callable, *args):
    """Run a blocking function without blocking the event loop (asyncio.to_thread)."""
    return await asyncio.to_thread(func, *args)


class SafeCounter:
    """A counter that is safe to increment from many threads (threading.Lock)."""

    def __init__(self) -> None:
        self._value = 0
        self._lock = threading.Lock()

    def increment(self) -> None:
        with self._lock:
            self._value += 1

    @property
    def value(self) -> int:
        return self._value


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
    for attempt in range(attempts):
        try:
            return operation()
        except TransientError:
            if attempt == attempts - 1:
                raise
            sleep(base_delay * 2 ** attempt)
    raise ValueError("attempts must be at least 1")


def jittered_delays(attempts: int, base: float, seed: int) -> list[float]:
    """Full-jitter backoff: delay n is uniform in [0, base * 2**n]. Same seed -> same delays."""
    rng = random.Random(seed)
    return [rng.uniform(0, base * 2 ** n) for n in range(attempts)]


class IdempotentPayments:
    """charge(key, amount) runs the side effect once per key; duplicates return the first result.

    Reusing a key with a DIFFERENT amount raises ValueError.
    """

    def __init__(self, charge_card: Callable[[float], str]):
        self._charge_card = charge_card
        self._results: dict[str, tuple[float, str]] = {}

    def charge(self, key: str, amount: float) -> str:
        if key in self._results:
            previous_amount, receipt = self._results[key]
            if previous_amount != amount:
                raise ValueError("idempotency key reused with different parameters")
            return receipt
        receipt = self._charge_card(amount)
        self._results[key] = (amount, receipt)
        return receipt
