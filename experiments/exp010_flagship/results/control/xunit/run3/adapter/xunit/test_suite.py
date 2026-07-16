# file: xunit/test_suite.py
from candidate import TestSuite as CandidateTestSuite


class TestSuite(CandidateTestSuite):
    def add(self, case):
        return self.add_case(case)
