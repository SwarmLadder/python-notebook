"""Independent build submissions from Basics 00, 04, 06, 10, 15, 16 and 17.

Complete each named build in its lesson, then copy your work here for
achievement verification. Do not change function names or interfaces.
"""


# Basics 00: create the requested session label.
session_label = None

# Basics 04: format each item and unit count independently.
def receipt(item: str, units: int) -> str:
    """Return '<item> x <units>' using the original item text, even for zero units."""
    raise NotImplementedError


def scan_batch(events: str) -> int:
    """Count uppercase A before the first batch-close marker |."""
    raise NotImplementedError


def invoice_total(lines, fee=0) -> int:
    """Bill line totals and one fee only for an order containing units."""
    raise NotImplementedError


def first_shortfall(stock, target):
    """Return the first index with stock strictly below target, or None."""
    raise NotImplementedError


def pack_runs(events: str) -> list[tuple[str, int]]:
    """Compress consecutive equal event codes without reordering."""
    raise NotImplementedError


def stock_report(rows):
    """Return (nonnegative totals by SKU, rejected input-row count)."""
    raise NotImplementedError
