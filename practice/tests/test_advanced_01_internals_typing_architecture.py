from datetime import datetime, timedelta

import pytest

from practice_loader import module_for

m = module_for(__file__)


def test_read_only_bag():
    source = [1, 2, 3, 4]
    bag = m.ReadOnlyBag(source)
    source.append(99)
    assert len(bag) == 4 and list(bag) == [1, 2, 3, 4], "copy the input"
    assert 3 in bag and 99 not in bag
    assert repr(bag) == "ReadOnlyBag([1, 2, 3, ...])"
    assert repr(m.ReadOnlyBag("ab")) == "ReadOnlyBag(['a', 'b'])"
    assert not hasattr(bag, "append")


def test_ticket_ordering_and_hashing():
    tickets = [m.Ticket(2, 1), m.Ticket(1, 5), m.Ticket(1, 2)]
    assert [(t.priority, t.sequence) for t in sorted(tickets)] == [(1, 2), (1, 5), (2, 1)]
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
    assert stack.pop() == 2 and stack.pop() == 1
    with pytest.raises(IndexError):
        stack.pop()


def test_first_or_none():
    assert m.first_or_none([4, 5]) == 4
    assert m.first_or_none("xyz") == "x"
    assert m.first_or_none([]) is None


def test_plugin_registry():
    registry = m.PluginRegistry(allowed={"upper", "reverse"})
    registry.register("upper", str.upper)
    assert registry.run("upper", "hi") == "HI"
    with pytest.raises(ValueError):
        registry.register("os_system", print)
    with pytest.raises(KeyError):
        registry.run("reverse", "abc")
    assert registry.names() == ["upper"]


def test_parameter_defaults():
    def connect(host, port=5432, *, timeout=2.5, ssl=None):
        pass
    assert m.parameter_defaults(connect) == {"host": None, "port": 5432, "timeout": 2.5, "ssl": None}


def test_rename_user_with_in_memory_repository():
    repo = m.InMemoryUserRepository()
    repo.save({"id": "u1", "name": "Ana"})
    assert m.rename_user(repo, "u1", "  Ana Maria ") == {"id": "u1", "name": "Ana Maria"}
    assert repo.get("u1")["name"] == "Ana Maria"
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
    assert repo.saved == [{"id": "u9", "name": "new"}]


def test_session_with_fake_clock():
    start = datetime(2024, 1, 1, 12, 0)
    now = [start]
    session = m.Session(created_at=start, ttl=timedelta(minutes=30), clock=lambda: now[0])
    assert not session.is_expired()
    now[0] = start + timedelta(minutes=29, seconds=59)
    assert not session.is_expired()
    now[0] = start + timedelta(minutes=30)
    assert session.is_expired()
