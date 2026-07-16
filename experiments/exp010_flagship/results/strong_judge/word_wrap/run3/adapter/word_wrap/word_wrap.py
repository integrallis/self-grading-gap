# file: word_wrap/word_wrap.py
from candidate import text_wrap


class WordWrap:
    def wrap(self, text, width):
        return text_wrap(text, width)
