import argparse
from textwrap import dedent

from aggregator import constants, db, utils

if __name__ == "__main__":

    def get_args():
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=dedent(
                """
                Grabs courses from the DB.
                """
            ),
        )
        parser.add_argument(
            "-d",
            "--difficulty",
            choices=constants.course_DIFFICULTIES,
            dest="difficulty",
            type=str,
            help="Restricts difficulty to the supplied input",
        )
        parser.add_argument(
            "-s",
            "--wanted_count",
            dest="wanted_count",
            type=int,
            help="Sets the minimum number of wanteds powerups",
        )
        parser.add_argument(
            "-c",
            "--count",
            default=1,
            dest="count",
            type=int,
            help="Increases the number of courses retrieved",
        )
        parser.add_argument(
            "--code",
            dest="code",
            type=str,
            help="Course code of course to retrieve. Ignores all usual seen operations",
        )
        parser.add_argument(
            "--unplay",
            action="store_true",
            default=False,
            dest="unplay",
            help="If --unplay and --code are supplied, marks supplied course as played=0",
        )
        parser.add_argument(
            "-n",
            "--db-name",
            default=db.DB_NAME,
            dest="db_name",
            help="The name of the DB. Specifies which DB you want to operate on.",
        )
        return parser.parse_args()

    args = vars(get_args())
    args["code"] = utils.format_course_code(args.get("code"))

    database = db.Db(args["db_name"])
    formatter = db.RowFormatter()

    if args.get("code"):
        results = database.get_by_course_code(args, formatter.format_courses)
    else:
        results = database.get_courses(args, formatter.format_courses)

    summary_results = database.get_db_summary(formatter.format_summary)

    print(summary_results)
    print(results)
