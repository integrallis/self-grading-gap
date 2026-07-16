# file: calculator_tdd_ebook/any.py
from candidate import DigitGenerator as _DigitGenerator


class Any:
    @classmethod
    def string_consisting_of(cls, *arguments):
        return _DigitGenerator().get_digit(*arguments)

    @classmethod
    def raises(cls, argument):
        return _DigitGenerator().get_digit(other_than=argument)
