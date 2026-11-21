import dataclasses
import logging
import typing

import pytest

from grader import check
from practice_loader import module_for

m = module_for(__file__)


def test_mean_or_none():
    check(m.mean_or_none([1, 2, 3, 4]))
    check(m.mean_or_none([]))


def test_product_record_typed_dict():
    assert typing.is_typeddict(m.ProductRecord)
    check(sorted(m.ProductRecord.__annotations__))


def test_apply_transform():
    rows = [{"price": 1}, {"price": 2}]
    check(m.apply_transform(rows, lambda r: {**r, "price": r["price"] * 10}))

    seen = []
    def mark(row):
        seen.append(row["id"])
        return {"seen": row["id"]}
    assert m.apply_transform(iter([{"id": "B"}, {"id": "A"}]), mark) == [{"seen": "B"}, {"seen": "A"}]
    assert seen == ["B", "A"], "Transform each row exactly once, in order."


def test_settings_validation():
    assert m.Settings().timeout > 0
    assert m.Settings(timeout=1, retries=0).retries == 0
    for kwargs in ({"timeout": 0}, {"timeout": -1}, {"retries": -1}):
        with pytest.raises(ValueError):
            m.Settings(**kwargs)
    with pytest.raises(dataclasses.FrozenInstanceError):
        m.Settings().timeout = 9


@pytest.mark.parametrize("text", ["12", " 0 "])
def test_parse_quantity(text):
    check(m.parse_quantity(text))


def test_parse_quantity_rejects_negative():
    with pytest.raises(m.InvalidQuantity):
        m.parse_quantity("-3")


def test_parse_quantity_chains_the_original_error():
    with pytest.raises(m.InvalidQuantity) as caught:
        m.parse_quantity("twelve")
    assert isinstance(caught.value.__cause__, ValueError), "use `raise ... from error`"
    assert issubclass(m.InvalidQuantity, ValueError)


def test_log_request_hides_token(caplog):
    logger = logging.getLogger("practice.test")
    with caplog.at_level(logging.INFO, logger="practice.test"):
        m.log_request(logger, "https://api.example/items", "s3cr3t-T0KEN", 200)
    assert "https://api.example/items" in caplog.text and "200" in caplog.text
    assert "s3cr3t-T0KEN" not in caplog.text, "never write secrets to logs"


@pytest.mark.parametrize("code", ["AB-1234", "ab-1234", "AB-123", "XAB-1234", "AB-12345", "AB1234"])
def test_is_order_code(code):
    check(m.is_order_code(code), hint="the WHOLE string must match")


@pytest.mark.parametrize("text", ["Shipped on 2024-03-09 by courier", "no date here", "2023-12-31"])
def test_extract_date(text):
    check(m.extract_date(text))


@pytest.mark.parametrize("text", ["Call 555-1234 or 555-9876.", "Order 12345-67890"])
def test_redact_phones(text):
    check(m.redact_phones(text))


def test_parse_products():
    check(m.parse_products('{"products": [{"sku": "A"}]}'))
    for bad in ("not json", "[]", '{"products": {}}', "{}"):
        with pytest.raises(ValueError):
            m.parse_products(bad)


def test_clean_csv():
    check(m.clean_csv("name,price\npen,1.50\nink,oops\npad,\nbook,12\n"), hint="the header is line 1")


@pytest.mark.parametrize("title", ["Hello, World!  2024", "  Python -- Tips ", "ALL CAPS"])
def test_slugify(title):
    check(m.slugify(title))


def test_hashtags():
    check(m.hashtags("Learning #Python with #py #AI and #python"))
    check(m.hashtags("no tags"))


def test_parse_settings():
    text = "# comment\nhost = localhost\n\nport=8080\nname = a = b\n"
    check(m.parse_settings(text), hint="split on the FIRST '=' only")
    with pytest.raises(ValueError, match="line 2"):
        m.parse_settings("a = 1\nbroken\n")


def test_summarize_sales():
    rows = [{"region": "north", "amount": "10.50"}, {"region": "south", "amount": "n/a"},
            {"region": "north", "amount": "4.25"}, {"region": "south", "amount": "3"}]
    check(m.summarize_sales(rows))

    assert m.summarize_sales([]) == {}
    assert m.summarize_sales([{"region": "west"}, {"region": "east", "amount": "0"}]) == {"east": 0}, "Distinguish a missing amount from a valid zero."
