# file: string_helper/helper.py
from candidate import matches_opening_closing_pairs


class StringHelper:
    def are_first_and_last_two_chars_same(self, text):
        return matches_opening_closing_pairs(text)
