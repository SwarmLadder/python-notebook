from datetime import datetime, timedelta

import pytest

from grader import check
from practice_loader import module_for

m = module_for(__file__)


def test_read_only_bag():
    source = [1, 2, 3, 4]
    bag = m.ReadOnlyBag(source)
    source.append(99)
    assert len(bag) == 4 and list(bag) == [1, 2, 3, 4], "copy the input"
    assert 3 in bag and 99 not in bag
    check(repr(bag))
    check(repr(m.ReadOnlyBag("ab")))
    assert not hasattr(bag, "append")


def test_ticket_ordering_and_hashing():
    tickets = [m.Ticket(2, 1), m.Ticket(1, 5), m.Ticket(1, 2)]
    check([(t.priority, t.sequence) for t in sorted(tickets)])
    assert m.Ticket(1, 1, "a") == m.Ticket(1, 1, "b")
    assert len({m.Ticket(1, 1), m.Ticket(1, 1)}) == 1


def test_ticket_returns_not_implemented():
    ticket = m.Ticket(1, 1)
    assert ticket.__eq__("x") is NotImplemented
    assert ticket.__lt__(3) is NotImplemented
    assert (ticket == "x") is False
    with pytest.raises(TypeError):
        ticket < 3  # noqa: B015


def test_positive_int_descriptor():
    class Order:
        quantity = m.PositiveInt()
        boxes = m.PositiveInt()

        def __init__(self, quantity, boxes=1):
            self.quantity, self.boxes = quantity, boxes

    order = Order(3, 2)
    assert (order.quantity, order.boxes) == (3, 2), "each attribute needs its own storage name"
    assert isinstance(Order.quantity, m.PositiveInt), "class access should return the descriptor"
    other = Order(7)
    assert order.quantity == 3, "values must be stored per instance"
    for bad, error in ((0, ValueError), (-2, ValueError), (1.5, TypeError), ("3", TypeError), (True, TypeError)):
        with pytest.raises(error):
            other.quantity = bad


def test_generic_stack():
    stack: m.Stack[int] = m.Stack()
    stack.push(1)
    stack.push(2)
    assert len(stack) == 2
    check([stack.pop(), stack.pop()])
    with pytest.raises(IndexError):
        stack.pop()


@pytest.mark.parametrize("values", [[4, 5], "xyz", []])
def test_first_or_none(values):
    check(m.first_or_none(values))


def test_plugin_registry():
    registry = m.PluginRegistry(allowed={"upper", "reverse"})
    registry.register("upper", str.upper)
    check(registry.run("upper", "hi"))
    with pytest.raises(ValueError):
        registry.register("os_system", print)
    with pytest.raises(KeyError):
        registry.run("reverse", "abc")
    check(registry.names())


def test_parameter_defaults():
    def connect(host, port=5432, *, timeout=2.5, ssl=None):
        pass
    check(m.parameter_defaults(connect))


def test_rename_user_with_in_memory_repository():
    repo = m.InMemoryUserRepository()
    repo.save({"id": "u1", "name": "Ana"})
    check(m.rename_user(repo, "u1", "  Ana Maria "))
    check(repo.get("u1"))
    with pytest.raises(KeyError):
        m.rename_user(repo, "nobody", "X")
    with pytest.raises(ValueError):
        m.rename_user(repo, "u1", "  ")


def test_rename_user_works_with_any_repository():
    class FakeRepo:
        def __init__(self):
            self.saved = []

        def get(self, user_id):
            return {"id": user_id, "name": "old"}

        def save(self, user):
            self.saved.append(user)

    repo = FakeRepo()
    m.rename_user(repo, "u9", "new")
    check(repo.saved)


def test_session_with_fake_clock():
    start = datetime(2024, 1, 1, 12, 0)
    now = [start]
    session = m.Session(created_at=start, ttl=timedelta(minutes=30), clock=lambda: now[0])
    results = []
    for offset in (timedelta(0), timedelta(minutes=29, seconds=59), timedelta(minutes=30)):
        now[0] = start + offset
        results.append(session.is_expired())
    check(results)


def test_vector_arithmetic():
    a, b = m.Vector(3, 4), m.Vector(1, -2)
    check([repr(a + b), repr(a - b), repr(a * 2), repr(2 * a), abs(a)])
    assert a == m.Vector(3, 4) and a != b
    assert len({m.Vector(1, 1), m.Vector(1, 1)}) == 1
    with pytest.raises(TypeError):
        a + 1
    with pytest.raises(TypeError):
        a * "x"
    assert not hasattr(a, "__dict__"), "use __slots__"


def test_lru_cache():
    cache = m.LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    check(cache.get("a"))
    cache.put("c", 3)  # evicts the least recently used key
    check([cache.get("b"), cache.keys()])
    with pytest.raises(ValueError):
        m.LRUCache(0)


def test_plugin_init_subclass():
    class CsvExporter(m.Plugin):
        name = "csv-test"

    assert m.Plugin.registry["csv-test"] is CsvExporter
    with pytest.raises(TypeError):
        class Nameless(m.Plugin):
            pass
    with pytest.raises(TypeError):
        class Duplicate(m.Plugin):
            name = "csv-test"


def test_enforce_types():
    @m.enforce_types
    def repeat(text: str, times: int, sep="-"):
        return sep.join([text] * times)

    check(repeat("ab", 3))
    check(repeat(times=2, text="x", sep="+"))
    with pytest.raises(TypeError):
        repeat("ab", "3")
    with pytest.raises(TypeError):
        repeat(5, 1)
    assert repeat.__name__ == "repeat"
