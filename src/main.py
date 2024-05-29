from datetime import datetime
from subprocess import run
import sys

from apiclient import ApiClient
import constants
from course import Course
from db import Db, RowFormatter
import results
import runner
import utils
        
if __name__ == "__main__":
    
    client = ApiClient()
    
    database = Db()
    formatter = RowFormatter()
    
    args = runner.get_args()
    runner.start_script_for(args)
    
    i = 0
    while not runner.should_exit():
        difficulty = utils.get_difficulty(args.difficulty, i)
        
        utils.print_status(f"GETTING {difficulty} endless courses from API", runner.count_superball_courses)
        
        m1_courses_info = client.get_possible_levels(difficulty)        
        
        total_course_count = len(m1_courses_info)
        for course_count, course_info in enumerate(m1_courses_info):
            utils.print_status(f"FETCHING {difficulty} course from API {course_count + 1}/{total_course_count}", runner.count_superball_courses)
            course_id = course_info.get('course_id')
            
            client.get_level_data(course_id)
            
            utils.print_status(f"DECRYPTING course data for \"{course_info.get('name')}\"", runner.count_superball_courses)
            run(['./courseDecrypter', constants.ENCRYPTED_LEVEL_NAME, constants.DECRYPTED_LEVEL_NAME])
            utils.clear_decrypter_stdout()
            
            
            utils.print_status(f"PROCESSING course data for \"{course_info.get('name')}\"", runner.count_superball_courses)
            
            course = None
            with open(constants.DECRYPTED_LEVEL_NAME, 'rb') as course_data:
                course = Course(course_data, difficulty, course_id)
                
            if course.has_superball:
                runner.count_superball_courses += 1
                database.insert_new_course(course)
            
            if runner.should_exit():
                sys.exit()
        
        # Iterate through the level difficulties   
        i = i + 1 if i < (len(constants.LEVEL_DIFFICULTIES) - 1) else 0