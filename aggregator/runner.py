"""
Not really a good name for this file.
This code facilitates the inputs of the file and the
delayed shutoff of application.
"""

import atexit
import argparse
from datetime import datetime, timedelta
from textwrap import dedent

from aggregator import constants, db, results

count_wanted_courses = 0
files_to_close = list()


def get_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=dedent(
            """
            Fetches courses from SMM2 endless, downloads SMB1 tileset courses, and
            processes them to identify if they contain the wanted object.
            Inputs of the application indicate how long to run for.
            """
        ),
    )
    parser.add_argument(
        "-o",
        "--hours",
        default=0,
        dest="hours",
        help="Quantity of hours to run the script for.",
        type=int,
    )
    parser.add_argument(
        "-m",
        "--minutes",
        default=0,
        dest="minutes",
        help="Quantity of minutes to run the script for.",
        type=int,
    )
    parser.add_argument(
        "-s",
        "--seconds",
        default=0,
        dest="seconds",
        help="Quantity of seconds to run the script for.",
        type=int,
    )
    parser.add_argument(
        "-d",
        "--difficulty",
        choices=["e", "n", "ex", "sex"],
        default="",
        dest="difficulty",
        help="Difficulty of courses to search through. Options are 'e', 'n', 'ex', 'sex'. If undefined will randomly iterate over options.",
        type=str,
    )
    parser.add_argument(
        "-i",
        "--wanted_id",
        default=34,
        dest="wanted_id",
        help="The bit string of the object that courses should be searched for. See README.md for more information.",
        type=int,
    )
    parser.add_argument(
        "-f",
        "--wanted_flag",
        default=None,
        dest="wanted_flag_bits",
        help='The bit string flag of the object that courses should be searched for. See README.md for more information (e.g. "00000110000000000000000000000100")',
    )
    parser.add_argument(
        "-n",
        "--db-name",
        default=db.DB_NAME,
        dest="db_name",
        help="The name of the DB. Different DB names allows stores of courses containing different objects.",
    )
    return parser.parse_args()


def start_script_for(args):
    global end_datetime

    atexit.register(exit_register)

    if args.hours or args.minutes or args.seconds:
        end_datetime = datetime.now() + timedelta(
            hours=args.hours, minutes=args.minutes, seconds=args.seconds
        )

    else:
        raise Exception("Must supply an input to the script")


def should_exit():
    return end_datetime <= datetime.now()


def exit_register():
    for file_to_close in files_to_close:
        file_to_close.close()

    print(constants.ERASE_LINE, end="")
    print(
        f"Found {count_wanted_courses} new courses! {':)' if count_wanted_courses > 0 else ':('}"
    )
