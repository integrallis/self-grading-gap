# file: xunit/test_suite.py
from candidate import TestSuite as CandidateTestSuite


class TestSuite(CandidateTestSuite):
    def __init__(self):
        CandidateTestSuite.__init__(self, list())

    def add(self, case):
        return self.cases.append(case)
