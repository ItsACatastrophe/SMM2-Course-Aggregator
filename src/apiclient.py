import time
import requests
import json

import src.constants


class ApiException(Exception):
    def __init__(self, response, status_code):
        super().__init__(f"[{status_code}] - {response}")
        
class ApiClient():
    def retry_on_fail(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ApiException:
                time.sleep(10)
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
        response = requests.get(f"https://tgrcode.com/mm2/search_endless_mode?count=300&difficulty={difficulty}", timeout=30)
        
        if response.status_code != 200:
            raise ApiException(response.text, response.status_code)
        
        courses = response.json().get('courses')
        
        courses_info = list()
        for course in courses:
            if course.get('game_style_name') == 'SMB1':
                courses_info.append(course)
        
        return courses_info
    
    @api_wait
    @retry_on_fail
    def get_level_data(self, course_code):
        response = requests.get(f'https://tgrcode.com/mm2/level_data/{course_code}', timeout=30)
        with open(constants.ENCRYPTED_LEVEL_NAME, "wb") as course_file:
            course_file.write(response.content)