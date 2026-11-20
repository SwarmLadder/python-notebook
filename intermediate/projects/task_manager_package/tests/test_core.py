"""Tests: python -m unittest discover -s tests -v."""

import sqlite3
import unittest
from task_manager.core import add_task, complete_task, initialize, list_tasks, remove_task


class TaskManagerTests(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        initialize(self.connection)

    def tearDown(self):
        self.connection.close()

    def test_add(self):
        task_id = add_task(self.connection, "Study")
        self.assertEqual(list_tasks(self.connection), [(task_id, "Study", 0)])

    def test_reject_blank(self):
        with self.assertRaises(ValueError):
            add_task(self.connection, " ")

    def test_complete(self):
        task_id = add_task(self.connection, "Run tests")
        complete_task(self.connection, task_id)
        self.assertEqual(list_tasks(self.connection, completed=True)[0][1], "Run tests")

    def test_missing(self):
        with self.assertRaises(KeyError):
            complete_task(self.connection, 999)

    def test_remove(self):
        task_id = add_task(self.connection, "Remove me")
        remove_task(self.connection, task_id)
        self.assertEqual(list_tasks(self.connection), [])


if __name__ == "__main__":
    unittest.main()
