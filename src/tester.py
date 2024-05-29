import argparse
from subprocess import run
import sys
from textwrap import dedent

from apiclient import ApiClient
import constants
from course import Course
from datetime import datetime
import db
import results
import runner
import utils

def get_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=dedent(
            """
            Fetches a specific level from the API, runs it through the usual
            decryption and processing
            """
        ),
    )
    parser.add_argument(
        "-c",
        "--code",
        default=0,
        dest="code",
        required=True,
        help="Course code of course to test out",
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    client = ApiClient()
    
    client.get_level_data(args.code)
    
    run(['./courseDecrypter', constants.ENCRYPTED_LEVEL_NAME, constants.DECRYPTED_LEVEL_NAME])
    utils.clear_decrypter_stdout()
    
    course = None
    with open(constants.DECRYPTED_LEVEL_NAME, 'rb') as course_data:
        course = Course(course_data, 'test', args.code)
    
    # # objs = list(filter(lambda o: o.is_superball(), [*course.area_main.objects, *course.area_sub.objects]))
    
    # for obj in [*course.area_main.objects, *course.area_sub.objects]:
    #     if obj.is_superball():
    #         print(f"flag_binary: {bin(obj.child_flags)}")
    #         print(f'{obj.id} (True): ({obj.x}, {obj.y})')
    
    # print(f"--- Only care about under this")
    # for obj in filter(lambda o: o.x == 27 and o.y == 8, course.area_main.objects):
    #     if obj.is_superball():
    #         print(f"flag_binary out here: {bin(obj.child_flags)}")
    #         print(f'{obj.id} (True): ({obj.x}, {obj.y})')
    # print(f"count of superb balls: {len(objs)}")
    