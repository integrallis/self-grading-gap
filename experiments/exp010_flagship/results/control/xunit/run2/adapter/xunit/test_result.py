# file: xunit/test_result.py
from candidate import Tally


class TestResult(Tally):
    test_started = Tally.record_run
    test_failed = Tally.record_failure
