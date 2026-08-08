# file: xunit/test_result.py
from candidate import Tally


class TestResult(Tally):
    def test_started(self):
        return self.record_run()

    def test_failed(self):
        return self.record_failure()
