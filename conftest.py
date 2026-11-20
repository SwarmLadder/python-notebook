"""Repository-wide pytest settings: a time limit for every test.

A learner's infinite loop (a `while` whose condition never becomes false, an
iterator that never raises StopIteration, list() over an endless generator)
would otherwise make pytest run forever with no message. After TEST_TIMEOUT
seconds (default 10, override with the PYTEST_TIMEOUT environment variable)
the test fails with an explanation. Code stuck inside a C function cannot be
interrupted that way; for that case pytest.ini sets faulthandler_timeout, which
stops the run with "Timeout" and prints the line where the code was stuck.
"""
from __future__ import annotations

import os
import signal
import sys
import threading

import pytest

TEST_TIMEOUT = float(os.environ.get("PYTEST_TIMEOUT", "10"))

ADVICE = (
    "took longer than {seconds:g} s, so it was stopped. This usually means an infinite loop:\n"
    "  - a `while` loop whose condition never becomes False (did you update the variable?)\n"
    "  - an iterator whose __next__ never raises StopIteration\n"
    "  - list() or sum() over an endless generator such as itertools.count()\n"
    "Try your function by hand on the test input with a print() inside the loop."
)


class TestTookTooLong(AssertionError):
    """Raised inside a test that exceeded the time limit."""


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    if TEST_TIMEOUT <= 0:
        yield
        return
    use_signal = hasattr(signal, "setitimer") and threading.current_thread() is threading.main_thread()
    previous = None
    if use_signal:
        def on_timeout(signum, frame):
            raise TestTookTooLong(ADVICE.format(seconds=TEST_TIMEOUT))
        previous = signal.signal(signal.SIGALRM, on_timeout)
        signal.setitimer(signal.ITIMER_REAL, TEST_TIMEOUT)
    try:
        yield
    finally:
        if use_signal:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, previous)
