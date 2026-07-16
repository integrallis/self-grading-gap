# file: string_helper/helper.py
from candidate import check_bookended


class StringHelper:
    are_first_and_last_two_chars_same = staticmethod(check_bookended)
