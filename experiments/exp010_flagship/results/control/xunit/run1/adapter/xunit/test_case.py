# file: xunit/test_case.py
from candidate import TestCase as _CandidateTestCase


class TestCase:
    def __init__(self, check):
        self._implementation = _CandidateTestCase(check)

    def run(self, result):
        return self._implementation.run(self._implementation.name, result)
