from datetime import datetime
from subprocess import run
import sys

from aggregator import constants, results, runner, utils
from aggregator.apiclient import ApiClient
from aggregator.course import Course
from aggregator.db import Db, RowFormatter

if __name__ == "__main__":
    args = runner.get_args()

    database = Db(args.db_name)
    formatter = RowFormatter()

    client = ApiClient(Db)

    runner.start_script_for(args)

    i = 0
    while not runner.should_exit():
        difficulty = utils.get_difficulty(args.difficulty, i)

        utils.print_status(
            f"GETTING {difficulty} endless courses from API",
            runner.count_wanted_courses,
        )

        m1_courses_info = client.get_possible_courses(difficulty)

        total_course_count = len(m1_courses_info)
        for course_count, course_info in enumerate(m1_courses_info):
            utils.print_status(
                f"FETCHING {difficulty} course from API {course_count + 1}/{total_course_count}",
                runner.count_wanted_courses,
            )
            course_id = course_info.get("course_id")

            client.get_course_data(course_id)

            utils.print_status(
                f"DECRYPTING course data for \"{course_info.get('name')}\"",
                runner.count_wanted_courses,
            )
            run(
                [
                    "./courseDecryptor",
                    constants.ENCRYPTED_course_NAME,
                    constants.DECRYPTED_course_NAME,
                ]
            )
            utils.clear_decrypter_stdout()

            utils.print_status(
                f"PROCESSING course data for \"{course_info.get('name')}\"",
                runner.count_wanted_courses,
            )

            course = None
            with open(constants.DECRYPTED_course_NAME, "rb") as course_data:
                course = Course(
                    course_data,
                    difficulty,
                    course_id,
                    args.wanted_id,
                    args.wanted_flag_bits,
                )

            if course.has_wanted:
                runner.count_wanted_courses += 1
                database.insert_new_course(course)

            if runner.should_exit():
                sys.exit()

        # Iterate through the course difficulties
        i = i + 1 if i < (len(constants.course_DIFFICULTIES) - 1) else 0
