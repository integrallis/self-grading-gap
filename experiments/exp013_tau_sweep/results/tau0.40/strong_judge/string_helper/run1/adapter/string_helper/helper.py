# file: string_helper/helper.py
from candidate import check_bookended_text


class StringHelper:
    def are_first_and_last_two_chars_same(self, text):
        return check_bookended_text(text)
