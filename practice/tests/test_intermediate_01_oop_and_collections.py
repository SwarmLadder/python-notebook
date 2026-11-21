import dataclasses

import pytest

from grader import check
from practice_loader import module_for

m = module_for(__file__)


def test_discounted():
    prices = [10.0, 19.99, 0]
    check(m.discounted(prices, 10))
    assert prices == [10.0, 19.99, 0], "do not modify the input list"
    check(m.discounted([], 50))


@pytest.mark.parametrize("prices, percent", [([-1], 10), ([5], -1), ([5], 101)])
def test_discounted_rejects_bad_input(prices, percent):
    with pytest.raises(ValueError):
        m.discounted(prices, percent)


def test_index_by_sku():
    records = [{"sku": "A1", "name": "Pen"}, {"sku": "B2", "name": "Ink"}]
    assert m.index_by_sku(records)["B2"] is records[1]
    with pytest.raises(ValueError):
        m.index_by_sku(records + [{"sku": "A1", "name": "Dup"}])

    assert m.index_by_sku([]) == {}


def test_unique_usernames():
    check(m.unique_usernames([" Ana", "ana", "BEN ", "   ", ""]))


def test_flatten_grid():
    check(m.flatten_grid([[1, 2], [3, 4]]))
    check(m.flatten_grid([]))


@pytest.mark.parametrize("n", [0, 1, 3, 5, 1_000_000])
def test_sum_even_squares(n):
    check(m.sum_even_squares(n))


def test_book_loans():
    book = m.Book("978-0", "Dune")
    book.borrow()
    assert book.on_loan
    with pytest.raises(RuntimeError):
        book.borrow()
    book.return_book()
    assert not book.on_loan
    with pytest.raises(RuntimeError):
        book.return_book()


def test_account():
    acct = m.Account("Ana", 100)
    acct.deposit(50)
    acct.withdraw(30)
    check(acct.balance)
    with pytest.raises(ValueError):
        acct.withdraw(1000)
    with pytest.raises(ValueError):
        acct.deposit(-5)
    check(acct.balance, hint="failed operations must not change the balance")
    with pytest.raises(AttributeError):
        acct.balance = 1_000_000  # read-only property


def test_product_dataclass():
    assert dataclasses.is_dataclass(m.Product)
    check(m.Product("P1", 2.5, 4).total_value)
    assert m.Product("P2", 1) == m.Product("P2", 1), "dataclasses compare by value"
    with pytest.raises(ValueError):
        m.Product("P3", -1, 1)


def test_playlists_do_not_share_tracks():
    first, second = m.Playlist("a"), m.Playlist("b")
    first.add("song")
    assert second.tracks == [], "use field(default_factory=list), not a shared default"


def test_coordinate_is_frozen_and_hashable():
    point = m.Coordinate(1, 2)
    with pytest.raises(dataclasses.FrozenInstanceError):
        point.x = 5
    assert {point: "home"}[m.Coordinate(1, 2)] == "home"


def test_temperature_properties():
    temp = m.Temperature(100)
    check(temp.fahrenheit)
    temp.fahrenheit = 32
    check(temp.celsius)
    with pytest.raises(ValueError):
        temp.celsius = -300
    with pytest.raises(ValueError):
        m.Temperature(-274)

    with pytest.raises(ValueError):
        temp.fahrenheit = -500
    assert temp.celsius == 0, "Reject the update before changing the stored temperature."


def test_inventory_total():
    inv = m.Inventory()
    inv.add(m.Product("A", 2.0, 3))
    inv.add(m.Product("B", 1.5, 2))
    check(inv.total_value())
    assert len(inv) == 2
    with pytest.raises(ValueError):
        inv.add(m.Product("A", 9.0, 1))


def test_transpose():
    check(m.transpose([[1, 2, 3], [4, 5, 6]]))
    check(m.transpose([]))


def test_money():
    total = m.Money(1.10) + m.Money(2.25)
    check(total)
    assert isinstance(total, m.Money)
    with pytest.raises(ValueError):
        m.Money(1, "USD") + m.Money(1, "EUR")
    with pytest.raises(TypeError):
        m.Money(1) + 5  # __add__ must return NotImplemented
    with pytest.raises(dataclasses.FrozenInstanceError):
        total.amount = 0


def test_shapes_polymorphism():
    shapes = [m.Rectangle(2, 3), m.Circle(1)]
    assert all(isinstance(s, m.Shape) for s in shapes)
    check(m.total_area(shapes))
    check([s.describe() for s in shapes])
    with pytest.raises(NotImplementedError):
        m.Shape().area()


def test_shopping_cart():
    cart = m.ShoppingCart()
    cart.add("pen", 1.50, 2)
    cart.add("ink", 4.25)
    cart.add("pen", 1.50)
    check(cart.total())
    check(len(cart))
    check(list(cart))
    assert "ink" in cart and "paper" not in cart
    with pytest.raises(ValueError):
        cart.add("x", 1, 0)
