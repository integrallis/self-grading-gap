# file: xunit/test_result.py
from candidate import Tally as CandidateTally


class TestResult(CandidateTally):
    def test_started(self):
        return self.record_run()

    def test_failed(self):
        return self.record_failure()
