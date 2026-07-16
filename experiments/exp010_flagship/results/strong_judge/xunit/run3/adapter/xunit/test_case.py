# file: xunit/test_case.py
from candidate import TestCase as CandidateTestCase


class TestCase(CandidateTestCase):
    def __init__(self, check):
        CandidateTestCase.__init__(self, check.__name__, check)
