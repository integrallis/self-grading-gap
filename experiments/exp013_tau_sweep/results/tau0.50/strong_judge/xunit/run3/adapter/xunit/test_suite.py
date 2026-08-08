# file: xunit/test_suite.py
from candidate import TestSuite as CandidateTestSuite


class TestSuite(CandidateTestSuite):
    def __init__(self):
        super().__init__(list())

    def add(self, case):
        self.cases.append(case)
