# file: xunit/test_suite.py
from candidate import TestSuite as CandidateTestSuite


class TestSuite(CandidateTestSuite):
    def __init__(self):
        self.test_cases = []
        super().__init__(self.test_cases)

    def add(self, test_case):
        self.test_cases.append(test_case)
