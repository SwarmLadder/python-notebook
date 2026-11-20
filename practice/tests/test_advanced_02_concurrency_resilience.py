import asyncio
import threading
import time

import pytest

from practice_loader import module_for

m = module_for(__file__)


async def slow_double(value):
    await asyncio.sleep(0.01 * (5 - value))  # later inputs finish first
    return value * 2


def test_gather_in_order_keeps_input_order():
    assert asyncio.run(m.gather_in_order([1, 2, 3, 4], slow_double)) == [2, 4, 6, 8]


def test_gather_in_order_runs_concurrently():
    async def nap(_):
        await asyncio.sleep(0.05)
    started = time.perf_counter()
    asyncio.run(m.gather_in_order(range(10), nap))
    assert time.perf_counter() - started < 0.3, "the workers should overlap, not run one by one"


def test_gather_in_order_propagates_errors():
    async def maybe_fail(value):
        if value == 2:
            raise ValueError("bad")
        await asyncio.sleep(0.01)
        return value
    with pytest.raises(ExceptionGroup):
        asyncio.run(m.gather_in_order([1, 2, 3], maybe_fail))


def test_with_timeout():
    async def main():
        quick = await m.with_timeout(asyncio.sleep(0, result="done"), 1)
        slow = await m.with_timeout(asyncio.sleep(5), 0.01)
        return quick, slow
    assert asyncio.run(main()) == (("ok", "done"), ("timeout", None))


def test_run_bounded_limits_concurrency():
    async def work(value):
        await asyncio.sleep(0.01)
        return value + 1
    results, peak = asyncio.run(m.run_bounded(range(10), work, limit=3))
    assert results == list(range(1, 11))
    assert peak == 3


def test_pipeline():
    assert asyncio.run(m.pipeline(["a", "b", "c"], str.upper, maxsize=1)) == ["A", "B", "C"]
    assert asyncio.run(m.pipeline([], str.upper)) == []


def test_run_blocking_uses_a_thread():
    main_thread = threading.get_ident()
    worker_thread = asyncio.run(m.run_blocking(threading.get_ident))
    assert worker_thread != main_thread


def test_safe_counter():
    counter = m.SafeCounter()

    def hammer():
        for _ in range(2000):
            counter.increment()

    threads = [threading.Thread(target=hammer) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert counter.value == 16000


def test_retry_succeeds_after_transient_failures():
    calls, sleeps = [], []

    def flaky():
        calls.append(1)
        if len(calls) < 3:
            raise m.TransientError("try again")
        return "ok"

    assert m.retry(flaky, attempts=5, base_delay=0.1, sleep=sleeps.append) == "ok"
    assert sleeps == pytest.approx([0.1, 0.2]), "exponential backoff: base * 2**attempt"


def test_retry_gives_up():
    sleeps = []

    def always_down():
        raise m.TransientError("down")

    with pytest.raises(m.TransientError):
        m.retry(always_down, attempts=3, base_delay=1, sleep=sleeps.append)
    assert sleeps == [1, 2], "no sleep after the final attempt"


def test_retry_does_not_retry_permanent_errors():
    calls = []

    def broken():
        calls.append(1)
        raise m.PermanentError("404")

    with pytest.raises(m.PermanentError):
        m.retry(broken, attempts=5, sleep=lambda s: None)
    assert len(calls) == 1


def test_jittered_delays():
    delays = m.jittered_delays(5, base=0.5, seed=7)
    assert len(delays) == 5
    assert all(0 <= d <= 0.5 * 2 ** n for n, d in enumerate(delays))
    assert m.jittered_delays(5, base=0.5, seed=7) == delays
    assert m.jittered_delays(5, base=0.5, seed=8) != delays


def test_idempotent_payments():
    charged = []

    def charge_card(amount):
        charged.append(amount)
        return f"receipt-{len(charged)}"

    payments = m.IdempotentPayments(charge_card)
    first = payments.charge("order-1", 25.0)
    assert payments.charge("order-1", 25.0) == first
    assert charged == [25.0], "a duplicate request must not charge twice"
    assert payments.charge("order-2", 25.0) != first
    with pytest.raises(ValueError):
        payments.charge("order-1", 99.0)
