import pytest

from grader import check
from practice_loader import module_for

m = module_for(__file__)


@pytest.mark.parametrize("celsius", [100, -40, 0, 37])
def test_celsius_to_fahrenheit(celsius):
    check(m.celsius_to_fahrenheit(celsius))


@pytest.mark.parametrize("values", [[3, -2, 9, 0], [5]])
def test_min_max(values):
    check(m.min_max(values))


def test_min_max_empty():
    with pytest.raises(ValueError):
        m.min_max([])


def test_average():
    check(m.average([1, 2, 3, 4]))
    with pytest.raises(ValueError):
        m.average([])


@pytest.mark.parametrize("price, kwargs", [(10, {}), (10, {"tax_rate": 0.05}), (0, {}), (19.99, {})])
def test_price_with_tax(price, kwargs):
    check(m.price_with_tax(price, **kwargs), hint="the default rate is 20%")


@pytest.mark.parametrize("n", [-3, 0, 1, 2, 3, 4, 17, 21, 97, 7919, 7917])
def test_is_prime(n):
    check(m.is_prime(n))


@pytest.mark.parametrize("text", ["3.5", " 42 ", "-1e3", "abc", ""])
def test_parse_number(text):
    check(m.parse_number(text))


def test_check_percentage():
    check(m.check_percentage(0))
    check(m.check_percentage(100))
    for bad in (-0.5, 100.5):
        with pytest.raises(ValueError):
            m.check_percentage(bad)


def test_score_report():
    check(m.score_report(["Ana", "Ben"], [90, 72]))
    check(m.score_report([], []))


def test_roll_dice_is_reproducible():
    rolls = m.roll_dice(10, seed=42)
    assert len(rolls) == 10
    assert all(1 <= r <= 6 for r in rolls)
    assert m.roll_dice(10, seed=42) == rolls, "same seed must give the same rolls"
    assert m.roll_dice(10, seed=1) != rolls

    assert m.roll_dice(0, seed=42) == [], "Zero requested rolls produce no samples."


def test_write_and_read_lines(tmp_path):
    path = tmp_path / "notes.txt"
    m.write_lines(path, ["first", "second", "café ☕"])
    assert m.read_lines(path) == ["first", "second", "café ☕"]


def test_count_nonblank_lines(tmp_path):
    path = tmp_path / "text.txt"
    path.write_text("one\n\n   \ntwo\n\tthree\n", encoding="utf-8")
    check(m.count_nonblank_lines(path))


def test_csv_round_trip(tmp_path):
    path = tmp_path / "students.csv"
    m.write_students_csv(path, [{"name": "Ana", "grade": 91}, {"name": "Ben", "grade": 78}])
    check(path.read_text(encoding="utf-8").splitlines()[0], hint="write a header row")
    grades = m.read_grades(path)
    assert grades == {"Ana": 91, "Ben": 78}
    assert all(isinstance(g, int) for g in grades.values()), "convert grades with int()"


def test_tasks_round_trip(tmp_path):
    path = tmp_path / "tasks.txt"
    assert m.load_tasks(path) == [], "a missing file means there are no tasks yet"
    m.save_tasks(path, ["Buy milk", "Réviser 📚"])
    assert m.load_tasks(path) == ["Buy milk", "Réviser 📚"]


@pytest.mark.parametrize("a, b", [(10, 4), (1, 0), (0, 5)])
def test_safe_divide(a, b):
    check(m.safe_divide(a, b))


@pytest.mark.parametrize("numbers", [(1, 2, 3), (), (10,)])
def test_describe_star_args(numbers):
    check(m.describe(*numbers))


def test_discount_price_is_keyword_only():
    check(m.discount_price(50))
    check(m.discount_price(50, percent=25))
    with pytest.raises(TypeError):
        m.discount_price(50, 25)
    with pytest.raises(ValueError):
        m.discount_price(50, percent=120)


def test_append_log(tmp_path):
    path = tmp_path / "log.txt"
    check(m.append_log(path, "started"))
    check(m.append_log(path, "finished"))
    assert path.read_text(encoding="utf-8") == "started\nfinished\n"


def test_longest_word_in_file(tmp_path):
    path = tmp_path / "words.txt"
    path.write_text("the quick brown\nfox jumps over\n\nlazy dogs\n", encoding="utf-8")
    check(m.longest_word_in_file(path), hint="the first longest word wins ties")
    empty = tmp_path / "empty.txt"
    empty.write_text("", encoding="utf-8")
    check(m.longest_word_in_file(empty))

    path.write_text("paid reçu!\nship dock!", encoding="utf-8")
    assert m.longest_word_in_file(path) == "reçu!", "Keep the first longest token, including punctuation."
