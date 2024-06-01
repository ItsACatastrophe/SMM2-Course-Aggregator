import time
import unittest
from unittest.mock import MagicMock

import requests

from aggregator import apiclient, db


class MockResponse:
    def __init__(self, status_code, response_dict={}):
        self.status_code = status_code
        self.json_dict = response_dict
        self.text = "test"

    def json(self):
        return self.json_dict


class TestApiClient(unittest.TestCase):
    def setUp(self):
        self.db = db.Db()
        self.api_client = apiclient.ApiClient(self.db)

        self.db.get_course_by_code_and_name = MagicMock(return_value=[])

        # All API calls usually sleep 1s minimum, bad for unit test
        time.sleep = MagicMock()

    def test_get_possible_courses(self):
        response = MockResponse(
            200,
            {
                "courses": [
                    {"game_style_name": "SMB1"},
                    {"game_style_name": "NSMBU"},
                    {"game_style_name": "SMB1"},
                ]
            },
        )
        requests.get = MagicMock(return_value=response)

        course_list = self.api_client.get_possible_courses("e")

        self.assertTrue(requests.get.called)
        self.assertTrue(time.sleep.called)
        self.assertIs(len(course_list), 2)

        for name in map(lambda course: course.get("game_style_name"), course_list):
            self.assertEqual(name, "SMB1")

    def test_get_possible_courses_exists_already(self):
        response = MockResponse(200, {"courses": [{"game_style_name": "SMB1"}]})
        requests.get = MagicMock(return_value=response)

        self.db.get_course_by_code_and_name = MagicMock(
            return_value=[{"one": "element"}]
        )

        course_list = self.api_client.get_possible_courses("e")

        self.assertTrue(self.db.get_course_by_code_and_name.called)
        self.assertIs(len(course_list), 0)

    def test_get_possible_courses_fail(self):
        response = MockResponse(500)
        requests.get = MagicMock(return_value=response)

        try:
            self.api_client.get_possible_courses("e")
        except apiclient.ApiException:
            self.assertTrue(requests.get.called)
            self.assertTrue(time.sleep.called)

            # Two calls because fails retry once
            self.assertIs(requests.get.call_count, 2)
            # Two calls because fails have an additional wait because rate limiting
            self.assertIs(time.sleep.call_count, 2)
        else:
            self.fail("Should raise custom exception if non 200 status code")
