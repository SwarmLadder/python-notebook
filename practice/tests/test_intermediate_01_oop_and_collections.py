import dataclasses

import pytest

from practice_loader import module_for

m = module_for(__file__)


def test_discounted():
    prices = [10.0, 19.99, 0]
    assert m.discounted(prices, 10) == [9.0, 17.99, 0]
    assert prices == [10.0, 19.99, 0], "do not modify the input list"
    assert m.discounted([], 50) == []


@pytest.mark.parametrize("prices, percent", [([-1], 10), ([5], -1), ([5], 101)])
def test_discounted_rejects_bad_input(prices, percent):
    with pytest.raises(ValueError):
        m.discounted(prices, percent)


def test_index_by_sku():
    records = [{"sku": "A1", "name": "Pen"}, {"sku": "B2", "name": "Ink"}]
    assert m.index_by_sku(records)["B2"]["name"] == "Ink"
    with pytest.raises(ValueError):
        m.index_by_sku(records + [{"sku": "A1", "name": "Dup"}])


def test_unique_usernames():
    assert m.unique_usernames([" Ana", "ana", "BEN ", "   ", ""]) == ["ana", "ben"]


def test_flatten_grid():
    assert m.flatten_grid([[1, 2], [3, 4]]) == [1, 2, 3, 4]
    assert m.flatten_grid([]) == []


@pytest.mark.parametrize("n, expected", [(0, 0), (1, 0), (3, 4), (5, 20)])
def test_sum_even_squares(n, expected):
    assert m.sum_even_squares(n) == expected


def test_sum_even_squares_large_n_is_fast():
    assert m.sum_even_squares(1_000_000) == sum(x * x for x in range(0, 1_000_000, 2))


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
    assert acct.balance == 120
    with pytest.raises(ValueError):
        acct.withdraw(1000)
    with pytest.raises(ValueError):
        acct.deposit(-5)
    assert acct.balance == 120, "failed operations must not change the balance"
    with pytest.raises(AttributeError):
        acct.balance = 1_000_000  # read-only property


def test_product_dataclass():
    assert dataclasses.is_dataclass(m.Product)
    product = m.Product("P1", 2.5, 4)
    assert product.total_value == 10
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
    assert temp.fahrenheit == pytest.approx(212)
    temp.fahrenheit = 32
    assert temp.celsius == pytest.approx(0)
    with pytest.raises(ValueError):
        temp.celsius = -300
    with pytest.raises(ValueError):
        m.Temperature(-274)


def test_inventory_total():
    inv = m.Inventory()
    inv.add(m.Product("A", 2.0, 3))
    inv.add(m.Product("B", 1.5, 2))
    assert inv.total_value() == pytest.approx(9.0)
    assert len(inv) == 2
    with pytest.raises(ValueError):
        inv.add(m.Product("A", 9.0, 1))
