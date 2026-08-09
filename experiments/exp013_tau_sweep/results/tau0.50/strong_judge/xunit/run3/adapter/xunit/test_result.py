# file: xunit/test_result.py
from candidate import Tally


class TestResult(Tally):
    test_failed = Tally.record_failure
    test_started = Tally.record_run
