from random import randint

from aggregator import constants

i_offset = randint(0, 3)


def seek_get(data, offset, size):
    data.seek(offset)
    return data.read(size)


def print_status(print_text, count_superball_courses: int):
    print(
        f"{constants.ERASE_LINE}[Found {count_superball_courses} Superballs] - {print_text}",
        end="",
    )


def clear_decrypter_stdout():
    """
    Clears the stdout from the course decrypter program
    Not very elegant but it'll do.
    """
    print(constants.LINE_UP, end=constants.LINE_CLEAR)
    print(constants.LINE_UP, end=constants.LINE_CLEAR)


def get_difficulty(difficulty: str, loop: int):
    if difficulty == "":
        difficulty_index = (loop + i_offset) % len(constants.LEVEL_DIFFICULTIES)
        difficulty = constants.LEVEL_DIFFICULTIES[difficulty_index]

    return difficulty


# All internal course code usage format as FOOBARBAZ
def format_course_code(code: str):
    formatted_code = None
    if code:
        formatted_code = code.upper().replace("-", "")
    return formatted_code
