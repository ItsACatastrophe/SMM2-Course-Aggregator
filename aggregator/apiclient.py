import time
import requests
import json

from aggregator import constants


class ApiException(Exception):
    def __init__(self, response, status_code):
        super().__init__(f"[{status_code}] - {response}")


class ApiClient:
    def __init__(self, database):
        self.db = database

    def retry_on_fail(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ApiException:
                time.sleep(2)
                return func(*args, **kwargs)

        return wrapper

    def api_wait(func):
        def wrapper(*args, **kwargs):
            time.sleep(1)
            return func(*args, **kwargs)

        return wrapper

    @api_wait
    @retry_on_fail
    def get_possible_levels(self, difficulty):
        response = requests.get(
            f"https://tgrcode.com/mm2/search_endless_mode?count=300&difficulty={difficulty}",
            timeout=30,
        )

        if response.status_code != 200:
            raise ApiException(response.text, response.status_code)

        courses = response.json().get("courses")

        courses_info = list()
        for course in courses:
            is_correct_style = course.get("game_style_name") == "SMB1"
            is_not_collected = (
                len(
                    self.db.get_course_by_code_and_name(
                        course.get("name"), course.get("course_id")
                    )
                )
                == 0
            )

            if is_correct_style and is_not_collected:
                courses_info.append(course)

        return courses_info

    @api_wait
    @retry_on_fail
    def get_level_data(self, course_code):
        response = requests.get(
            f"https://tgrcode.com/mm2/level_data/{course_code}", timeout=15
        )
        if response.status_code == 400:
            raise Exception("get_level_data for code that does not exist")

        with open(constants.ENCRYPTED_LEVEL_NAME, "wb") as course_file:
            course_file.write(response.content)
