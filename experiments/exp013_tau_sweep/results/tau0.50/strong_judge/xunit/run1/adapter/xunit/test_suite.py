# file: xunit/test_suite.py
from candidate import Suite


class TestSuite(Suite):
    def __init__(self):
        super().__init__(list())

    def add(self, test_case):
        return self.test_cases.append(test_case)
