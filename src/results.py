import csv
import os

from src.course import Course

# TODO: I think I need to rethink how files are treated by the program.
# We write and read from the same file. Perhaps testing when data is saved
# after writing is in order?
# TODO: Rename this class, it does more than just writing, also reading and determining
# new levels
class Writer():
    SEEN_PATH = './results/seen.csv'
    SUPERBALL_COURSES_PATH = './results/superball_courses.csv'
    
    def __init__(self):
        is_new_seen_file = not os.path.exists(Writer.SEEN_PATH)
        is_new_superball_course_file = not os.path.exists(Writer.SUPERBALL_COURSES_PATH)
        
        if is_new_seen_file:
            seen_file = open(Writer.SEEN_PATH, 'w+')
            seen_writer = csv.DictWriter(seen_file, fieldnames=['course_code'])
            seen_writer.writeheader()
            seen_file.close()
            
        if is_new_superball_course_file:
            superball_file = open(Writer.SUPERBALL_COURSES_PATH, 'w+')
            superball_writer = csv.DictWriter(superball_file, fieldnames=Course.get_course_repr_keys())
            superball_writer.writeheader()
            superball_file.close()
    
    def get_unseen_courses(self, courses_info):
        """
        We should try to optimize this, making it use a generator
        for seen codes is the first step.
        """
        seen_file = open(Writer.SEEN_PATH, 'r')
        seen_codes = seen_file.read() # TODO: make this a generator, I worry for how large this file will get
        
        new_course_info = []   
        for course_info in courses_info:
            course_code = course_info.get("course_id")
            
            if not course_code in seen_codes:
                new_course_info.append(course_info)
                
        return new_course_info
    
    def write_seen_m1_course_id(self, course_code):
        self.seen_file = open(Writer.SEEN_PATH, 'a')
        self.seen_writer = csv.DictWriter(self.seen_file, fieldnames=['course_code'])
        self.seen_writer.writerow({'course_code': course_code})
        
        self.seen_file.close()
    
    def write_superball_course(self, course: Course):
        self.superball_file = open(Writer.SUPERBALL_COURSES_PATH, 'a')
        self.superball_writer = csv.DictWriter(self.superball_file, fieldnames=[*Course.get_course_repr_keys(), 'played'])
        
        course_summary = course.get_course_data() 
        self.superball_writer.writerow(course.get_course_data())
        
        self.superball_file.close()
        