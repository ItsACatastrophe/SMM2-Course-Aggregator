"""
Not really a good name for this file.
This code facilitates the inputs of the file and the
delayed shutoff of application.
"""
import atexit
import argparse
from datetime import datetime, timedelta
from textwrap import dedent

import src.constants
import src.results

count_superball_courses = 0

files_to_close = list()

def get_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=dedent(
            """
            Fetches levels from SMM2 endless, downloads SMB1 tileset levels, and
            processes them to identify if they contain a superball.
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
        help="Difficulty of levels to search through. Options are 'e', 'n', 'ex', 'sex'. If undefined will randomly iterate over options",
        type=str,
    )
    return parser.parse_args()

def start_script_for(args):
    global end_datetime
    
    atexit.register(exit_register)
    
    if args.hours or args.minutes or args.seconds :
        end_datetime = datetime.now() + timedelta(hours=args.hours, minutes=args.minutes, seconds=args.seconds)
        
    else:
        raise Exception('Must supply an input to the script')
    
def should_exit():
    return end_datetime <= datetime.now()

def exit_register():
    for file_to_close in files_to_close:
        file_to_close.close()
    
    print(constants.ERASE_LINE, end="") 
    print(f"Found {count_superball_courses} new levels with superballs! {':)' if count_superball_courses > 0 else ':('}")
    
        
        
        
        
        