import sqlite3
import unittest

from aggregator import constants, db


class TestFormatter(unittest.TestCase):
    def setUp(self):
        self.con = sqlite3.connect(":memory:")
        self.con.row_factory = sqlite3.Row

        self.formatter = db.RowFormatter()

    def test_format_summary(self):
        rows = self.con.execute("SELECT 'e' AS difficulty, 2 AS count ").fetchall()

        formatted_summary = self.formatter.format_summary(rows)

        self.assertIn("e", formatted_summary)
        self.assertIn("2", formatted_summary)

    def test_format_summary_order(self):
        # Only here to get Row objs back
        rows = self.con.execute(
            """
            SELECT 'e' AS difficulty, 2 AS count UNION
            SELECT 'sex' AS difficulty, 2 AS count UNION
            SELECT 'ex' AS difficulty, 2 AS count UNION
            SELECT 'n' AS difficulty, 2 AS count
            """
        ).fetchall()

        formatted_summary = self.formatter.format_summary(rows)

        # Checks if difficulties are in order
        indices = list(
            map(lambda d: formatted_summary.find(d), constants.LEVEL_DIFFICULTIES)
        )
        self.assertTrue(
            all(indices[i] < indices[i + 1] for i in range(len(indices) - 1))
        )

    def test_format_courses_single(self):
        rows = self.con.execute(
            """
            SELECT
                'test-name' as name, 
                'FOOBARBAZ' as code, 
                'n' as difficulty, 
                3 as superball_count
            """
        ).fetchall()

        formatted_course = self.formatter.format_courses(rows)

        self.assertIn("test-name", formatted_course)
        self.assertIn("FOO-BAR-BAZ", formatted_course)
        self.assertIn("(n)", formatted_course)
        self.assertIn("3", formatted_course)
