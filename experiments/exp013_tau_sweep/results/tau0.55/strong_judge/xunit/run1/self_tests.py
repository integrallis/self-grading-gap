from solution import Tally, TestCase, TestSuite

def test_tally_initial_state():
    tally = Tally()
    assert tally.runs == 0  # AC-1.1: fresh tally shows zero tests run
    assert tally.failures == 0  # AC-1.1: fresh tally shows zero failures

def test_tally_increment_run():
    tally = Tally()
    tally.record_run()
    assert tally.runs == 1  # AC-1.2: increment the run count by one

def test_tally_increment_failure():
    tally = Tally()
    tally.record_failure()
    assert tally.failures == 1  # AC-1.3: increment the failure count by one

def test_tally_multiple_failures():
    tally = Tally()
    tally.record_failure()
    tally.record_failure()
    assert tally.failures == 2  # AC-1.3: two failures count as two

def test_tally_summary_initial():
    tally = Tally()
    assert tally.summary() == "0 run, 0 failed"  # AC-1.4: fresh tally summary

def test_tally_summary_after_runs():
    tally = Tally()
    tally.record_run()
    tally.record_failure()
    assert tally.summary() == "1 run, 1 failed"  # AC-1.4: after one run, one failure

def test_tally_summary_after_multiple_runs():
    tally = Tally()
    tally.record_run()
    tally.record_run()
    tally.record_failure()
    assert tally.summary() == "2 run, 1 failed"  # AC-1.4: after two runs, one failure

def test_test_case_name():
    case = TestCase("example_check", lambda: True)
    assert case.name == "example_check"  # AC-2.1: check case exposes the name

def test_test_case_run_calls_check():
    events = []

    class ExampleCheck:
        def check(self):
            events.append("check")

    tally = Tally()
    case = TestCase("example_check", ExampleCheck().check)
    case.run(tally)
    assert "check" in events  # AC-2.2: running a case invokes the named check

def test_test_case_run_records_failure():
    events = []

    class FailingCheck:
        def check(self):
            events.append("check")
            assert False  # This will fail

    tally = Tally()
    case = TestCase("failing_check", FailingCheck().check)
    case.run(tally)
    assert tally.runs == 1  # AC-2.3: still records the run
    assert tally.failures == 1  # AC-3.1: captures the failure
    assert "check" in events  # Ensure the check was called before failure

def test_test_case_setup_and_teardown():
    events = []

    class TestCheck:
        def setup(self):
            events.append("setup")

        def check(self):
            events.append("check")

        def teardown(self):
            events.append("teardown")

    case = TestCase("example_check", TestCheck().check)
    case.run(Tally())
    assert events == ["setup", "check", "teardown"]  # AC-2.4 & AC-2.5: correct order

def test_test_case_teardown_on_failure():
    events = []

    class FailingCheck:
        def setup(self):
            events.append("setup")

        def check(self):
            events.append("check")
            assert False  # This will fail

        def teardown(self):
            events.append("teardown")

    tally = Tally()
    case = TestCase("failing_check", FailingCheck().check)
    case.run(tally)
    assert events == ["setup", "check", "teardown"]  # Correct order even on failure
    assert tally.failures == 1  # AC-3.1: failure is counted

def test_test_suite_runs_cases():
    tally = Tally()
    suite = TestSuite()
    case1 = TestCase("passing_check_1", lambda: True)
    case2 = TestCase("passing_check_2", lambda: True)
    suite.add_case(case1)
    suite.add_case(case2)
    suite.run(tally)
    assert tally.runs == 2  # AC-4.1: two passing cases yield two runs
    assert tally.failures == 0  # AC-4.1: zero failures
    assert tally.summary() == "2 run, 0 failed"  # Ensure summary is correct

def test_test_suite_with_failure_then_pass():
    tally = Tally()
    suite = TestSuite()
    
    class FailingCheck:
        def check(self):
            assert False  # This will fail

    class PassingCheck:
        def check(self):
            pass  # This will pass

    case1 = TestCase("failing_check", FailingCheck().check)
    case2 = TestCase("passing_check", PassingCheck().check)
    suite.add_case(case1)
    suite.add_case(case2)
    suite.run(tally)
    assert tally.runs == 2  # Both cases ran
    assert tally.failures == 1  # One failure
    assert tally.summary() == "2 run, 1 failed"  # Summary after failure and pass

def test_empty_suite():
    tally = Tally()
    suite = TestSuite()
    suite.run(tally)
    assert tally.summary() == "0 run, 0 failed"  # AC-4.1: empty suite summary