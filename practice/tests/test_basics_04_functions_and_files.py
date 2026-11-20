import pytest

from practice_loader import module_for

m = module_for(__file__)


def test_celsius_to_fahrenheit():
    assert m.celsius_to_fahrenheit(100) == 212
    assert m.celsius_to_fahrenheit(-40) == -40
    assert m.celsius_to_fahrenheit.__doc__, "add a docstring that explains the function"


def test_min_max():
    assert tuple(m.min_max([3, -2, 9, 0])) == (-2, 9)
    assert tuple(m.min_max([5])) == (5, 5)
    with pytest.raises(ValueError):
        m.min_max([])


def test_average():
    assert m.average([1, 2, 3, 4]) == 2.5
    with pytest.raises(ValueError):
        m.average([])


def test_price_with_tax():
    assert m.price_with_tax(10) == 12.0
    assert m.price_with_tax(10, tax_rate=0.05) == 10.5
    assert m.price_with_tax(0) == 0


@pytest.mark.parametrize("n, expected", [(-3, False), (0, False), (1, False), (2, True), (3, True), (4, False),
                                          (17, True), (21, False), (97, True), (7919, True), (7917, False)])
def test_is_prime(n, expected):
    assert m.is_prime(n) is expected


@pytest.mark.parametrize("text, expected", [("3.5", 3.5), (" 42 ", 42.0), ("-1e3", -1000.0), ("abc", None), ("", None)])
def test_parse_number(text, expected):
    assert m.parse_number(text) == expected


def test_check_percentage():
    assert m.check_percentage(0) == 0
    assert m.check_percentage(100) == 100
    for bad in (-0.5, 100.5):
        with pytest.raises(ValueError):
            m.check_percentage(bad)


def test_score_report():
    assert m.score_report(["Ana", "Ben"], [90, 72]) == ["1. Ana: 90", "2. Ben: 72"]
    assert m.score_report([], []) == []


def test_roll_dice_is_reproducible():
    rolls = m.roll_dice(10, seed=42)
    assert len(rolls) == 10
    assert all(1 <= r <= 6 for r in rolls)
    assert m.roll_dice(10, seed=42) == rolls, "same seed must give the same rolls"
    assert m.roll_dice(10, seed=1) != rolls


def test_write_and_read_lines(tmp_path):
    path = tmp_path / "notes.txt"
    m.write_lines(path, ["first", "second", "café ☕"])
    assert m.read_lines(path) == ["first", "second", "café ☕"]


def test_count_nonblank_lines(tmp_path):
    path = tmp_path / "text.txt"
    path.write_text("one\n\n   \ntwo\n\tthree\n", encoding="utf-8")
    assert m.count_nonblank_lines(path) == 3


def test_csv_round_trip(tmp_path):
    path = tmp_path / "students.csv"
    m.write_students_csv(path, [{"name": "Ana", "grade": 91}, {"name": "Ben", "grade": 78}])
    assert path.read_text(encoding="utf-8").splitlines()[0] == "name,grade"
    grades = m.read_grades(path)
    assert grades == {"Ana": 91, "Ben": 78}
    assert all(isinstance(g, int) for g in grades.values()), "convert grades with int()"


def test_tasks_round_trip(tmp_path):
    path = tmp_path / "tasks.txt"
    assert m.load_tasks(path) == [], "a missing file means there are no tasks yet"
    m.save_tasks(path, ["Buy milk", "Réviser 📚"])
    assert m.load_tasks(path) == ["Buy milk", "Réviser 📚"]
