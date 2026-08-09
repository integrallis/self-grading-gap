# file: word_wrap/word_wrap.py
from candidate import wrap_text


class WordWrap:
    def wrap(self, text, width):
        return wrap_text(text, width)
