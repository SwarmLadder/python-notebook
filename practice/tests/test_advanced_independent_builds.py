"""Independent engineering acceptance tests across resilience and performance."""
import pytest
from practice_loader import module_for

m = module_for(__file__)


@pytest.mark.parametrize("total,workers", [(0, 1), (0, 5), (1, 3), (7, 3), (9, 4), (17, 1), (22, 7)])
def test_split_jobs(total, workers):
    spans = m.split_jobs(total, workers)
    assert isinstance(spans, list) and len(spans) == workers, "Return one interval per worker"
    assert all(type(a) is int and type(b) is int and a <= b for a, b in spans)
    assert spans[0][0] == 0 and spans[-1][1] == total
    assert all(spans[i][1] == spans[i + 1][0] for i in range(workers - 1)), "No gaps or overlaps"
    sizes = [b - a for a, b in spans]
    assert max(sizes) - min(sizes) <= 1
    assert sizes == sorted(sizes, reverse=True), "Earlier workers receive any extra jobs"


@pytest.mark.parametrize("workers", [0, -1])
def test_split_jobs_bad_workers(workers):
    with pytest.raises(ValueError):
        m.split_jobs(3, workers)


@pytest.mark.parametrize("samples,expected", [
    ([], 0), ([8], 0), ([9, 6, 13, 8], 4), ([9, 3], 0),
    ([-5, -2, -10], 3), ([3, 3, 3], 0), ([4, 8, 6, 13], 9),
])
def test_peak_delta(samples, expected):
    assert m.peak_delta(iter(samples)) == expected, "Measure peaks above the FIRST sample"


def test_peak_delta_one_pass():
    def readings():
        yield 100
        yield 70
        yield 105
    assert m.peak_delta(readings()) == 5


def _correct_deliver():
    seen = set()
    def deliver(key):
        fresh = key not in seen
        seen.add(key)
        return fresh
    return deliver


def _last_only():
    last = [None]
    def deliver(key):
        fresh = key != last[0]
        last[0] = key
        return fresh
    return deliver


def _always_true():
    return lambda key: True


def _always_false():
    return lambda key: False


def test_test_replay():
    assert m.test_replay(_correct_deliver()) is None, "Do not reject a correct replay service"
    for broken in (_last_only, _always_true, _always_false):
        with pytest.raises(AssertionError):
            m.test_replay(broken())


@pytest.mark.parametrize("events,expected", [
    ([], (0, 0, 0)),
    ([("A", 5), ("B", 0), ("A", 6), ("A", 5), ("B", 0)], (5, 2, 1)),
    ([("X", 4), ("X", 4), ("X", 4)], (4, 2, 0)),
    ([("A", 2), ("A", 3), ("A", 3), ("B", 7)], (9, 0, 2)),
    ([("Q", 0), ("Q", 1), ("R", 10), ("Q", 0)], (10, 1, 1)),
])
def test_replay_summary(events, expected):
    assert m.replay_summary(iter(events)) == expected, "Only the first amount per key is accepted"
