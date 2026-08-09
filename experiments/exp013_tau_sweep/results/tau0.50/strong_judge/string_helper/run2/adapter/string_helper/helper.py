# file: string_helper/helper.py
from candidate import matches_opening_closing_pairs


class StringHelper:
    are_first_and_last_two_chars_same = staticmethod(matches_opening_closing_pairs)
