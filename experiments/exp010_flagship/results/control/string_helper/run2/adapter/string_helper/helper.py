# file: string_helper/helper.py
from candidate import matching_pairs


class StringHelper:
    def are_first_and_last_two_chars_same(self, text):
        return matching_pairs(text)
