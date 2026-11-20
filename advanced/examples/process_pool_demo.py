"""Portable process pool demonstration.

Run as a standalone script:
    python advanced/examples/process_pool_demo.py

Interactive notebooks are not always suitable for spawning process workers,
especially with the spawn start method. Keep workers importable at module scope.
"""
from concurrent.futures import ProcessPoolExecutor


def sum_of_squares(limit: int) -> int:
    if limit < 0:
        raise ValueError("limit must not be negative")
    return sum(number * number for number in range(limit))


def main() -> None:
    limits = [100, 200, 300]
    with ProcessPoolExecutor(max_workers=2) as pool:
        actual = list(pool.map(sum_of_squares, limits))
    expected = [sum_of_squares(limit) for limit in limits]
    assert actual == expected
    print("Parallel results:", actual)


if __name__ == "__main__":
    main()
