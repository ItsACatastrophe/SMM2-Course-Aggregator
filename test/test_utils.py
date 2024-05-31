import unittest

from aggregator import utils


class TestUtils(unittest.TestCase):
    def test_format_course_code(self):
        level_code = "foO-Bar-Baz"

        formatted_code = utils.format_course_code(level_code)

        self.assertTrue(formatted_code.isupper())
        self.assertNotIn("-", formatted_code)
