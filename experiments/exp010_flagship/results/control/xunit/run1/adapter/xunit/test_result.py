# file: xunit/test_result.py
from candidate import Tally as _Tally


class TestResult(_Tally):
    def test_started(self):
        return self.record_run()

    def test_failed(self):
        return self.record_failure()
