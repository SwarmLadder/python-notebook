"""Run with PYTHONPATH=src python -m unittest discover -s tests -v."""

import sqlite3
import unittest

from event_processor.core import Event, apply_event, category_totals, initialize, parse_event


class EventTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        initialize(self.db)

    def tearDown(self):
        self.db.close()

    def test_accept_and_replay(self):
        event = Event("E1", "books", 5)
        self.assertEqual(apply_event(self.db, event), "accepted")
        self.assertEqual(apply_event(self.db, event), "replayed")
        self.assertEqual(category_totals(self.db), {"books": 5})

    def test_conflict(self):
        apply_event(self.db, Event("E1", "books", 5))
        with self.assertRaises(ValueError):
            apply_event(self.db, Event("E1", "books", 10))
        self.assertEqual(category_totals(self.db), {"books": 5})

    def test_aggregate(self):
        apply_event(self.db, Event("E1", "books", 2))
        apply_event(self.db, Event("E2", "books", 3))
        self.assertEqual(category_totals(self.db)["books"], 5)

    def test_invalid_amount(self):
        with self.assertRaises(ValueError):
            Event("E1", "books", -1)
        with self.assertRaises(ValueError):
            Event("E1", "books", True)

    def test_missing_field(self):
        with self.assertRaises(ValueError):
            parse_event({"event_id": "E1", "amount": 2})


if __name__ == "__main__":
    unittest.main()
