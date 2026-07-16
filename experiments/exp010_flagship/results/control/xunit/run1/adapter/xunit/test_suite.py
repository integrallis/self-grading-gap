# file: xunit/test_suite.py
from candidate import TestSuite as _CandidateTestSuite


class TestSuite:
    def __init__(self):
        self._implementation = _CandidateTestSuite()

    def add(self, test_case):
        return self._implementation.add(test_case._implementation)

    def run(self, result):
        return self._implementation.run(result)
