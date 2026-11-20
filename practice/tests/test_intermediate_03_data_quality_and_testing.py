import dataclasses
import logging
import typing

import pytest

from practice_loader import module_for

m = module_for(__file__)


def test_mean_or_none():
    assert m.mean_or_none([1, 2, 3, 4]) == 2.5
    assert m.mean_or_none([]) is None


def test_mean_or_none_is_annotated():
    hints = typing.get_type_hints(m.mean_or_none)
    assert "values" in hints and "return" in hints, "annotate the parameter and the return type"


def test_product_record_typed_dict():
    assert typing.is_typeddict(m.ProductRecord)
    assert set(m.ProductRecord.__annotations__) == {"sku", "name", "price"}


def test_apply_transform():
    rows = [{"price": 1}, {"price": 2}]
    assert m.apply_transform(rows, lambda r: {**r, "price": r["price"] * 10}) == [{"price": 10}, {"price": 20}]


def test_settings_validation():
    assert m.Settings().timeout > 0
    assert m.Settings(timeout=1, retries=0).retries == 0
    for kwargs in ({"timeout": 0}, {"timeout": -1}, {"retries": -1}):
        with pytest.raises(ValueError):
            m.Settings(**kwargs)
    with pytest.raises(dataclasses.FrozenInstanceError):
        m.Settings().timeout = 9


def test_parse_quantity():
    assert m.parse_quantity("12") == 12
    assert m.parse_quantity(" 0 ") == 0
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


@pytest.mark.parametrize("code, ok", [("AB-1234", True), ("ab-1234", False), ("AB-123", False),
                                       ("XAB-1234", False), ("AB-12345", False), ("AB1234", False)])
def test_is_order_code(code, ok):
    assert m.is_order_code(code) is ok


def test_extract_date():
    assert m.extract_date("Shipped on 2024-03-09 by courier") == {"year": 2024, "month": 3, "day": 9}
    assert m.extract_date("no date here") is None


def test_redact_phones():
    assert m.redact_phones("Call 555-1234 or 555-9876.") == "Call [PHONE] or [PHONE]."
    assert m.redact_phones("Order 12345-67890") == "Order 12345-67890"


def test_parse_products():
    assert m.parse_products('{"products": [{"sku": "A"}]}') == [{"sku": "A"}]
    for bad in ("not json", "[]", '{"products": {}}', "{}"):
        with pytest.raises(ValueError):
            m.parse_products(bad)


def test_clean_csv():
    text = "name,price\npen,1.50\nink,oops\npad,\nbook,12\n"
    rows, rejected = m.clean_csv(text)
    assert rows == [{"name": "pen", "price": 1.5}, {"name": "book", "price": 12.0}]
    assert rejected == [3, 4]
