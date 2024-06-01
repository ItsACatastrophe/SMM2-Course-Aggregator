import unittest

from aggregator import utils


class TestUtils(unittest.TestCase):
    def test_format_course_code(self):
        course_code = "foO-Bar-Baz"

        formatted_code = utils.format_course_code(course_code)

        self.assertTrue(formatted_code.isupper())
        self.assertNotIn("-", formatted_code)
