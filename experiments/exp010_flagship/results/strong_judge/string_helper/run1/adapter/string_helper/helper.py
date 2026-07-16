# file: string_helper/helper.py
from candidate import match_bookended_text


class StringHelper:
    are_first_and_last_two_chars_same = staticmethod(match_bookended_text)
