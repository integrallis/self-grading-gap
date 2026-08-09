from solution import Tally, TestCase, TestSuite

def test_initial_tally():
    tally = Tally()
    assert tally.runs == 0  # AC-1.1
    assert tally.failures == 0  # AC-1.1
    assert tally.summary() == "0 run, 0 failed"  # AC-1.4

def test_record_run_increments_run_count():
    tally = Tally()
    tally.record_run()
    assert tally.runs == 1  # AC-1.2
    assert tally.failures == 0  # AC-1.2

def test_record_failure_increments_failure_count():
    tally = Tally()
    tally.record_run()
    tally.record_failure()
    assert tally.runs == 1  # AC-1.3
    assert tally.failures == 1  # AC-1.3

def test_record_two_failures_increments_failure_count():
    tally = Tally()
    tally.record_run()
    tally.record_failure()
    tally.record_run()
    tally.record_failure()
    assert tally.runs == 2  # Two runs recorded
    assert tally.failures == 2  # Two failures recorded

def test_tally_summary():
    tally = Tally()
    assert tally.summary() == "0 run, 0 failed"  # AC-1.4
    tally.record_run()
    tally.record_failure()
    assert tally.summary() == "1 run, 1 failed"  # AC-1.4
    tally.record_run()
    assert tally.summary() == "2 run, 1 failed"  # AC-1.4

def test_test_case_exposes_name():
    case = TestCase("example_test")
    assert case.name == "example_test"  # AC-2.1

def test_test_case_runs_check():
    check_called = [False]
    tally = Tally()
    case = TestCase("example_test", lambda: check_called.__setitem__(0, True), tally)
    case.run()
    assert check_called[0]  # Check was invoked

def test_test_case_records_run_in_tally():
    tally = Tally()
    case = TestCase("example_test", lambda: None, tally)
    case.run()
    assert tally.summary() == "1 run, 0 failed"  # AC-2.3

def test_test_case_runs_setup_before_check():
    event_order = []

    def setup():
        event_order.append("setup")

    def check():
        event_order.append("check")

    case = TestCase("example_test", check, tally=Tally(), setup=setup)
    case.run()
    assert event_order == ["setup", "check"]  # AC-2.4 and AC-2.2

def test_test_case_runs_tear_down_after_check():
    event_order = []

    def teardown():
        event_order.append("teardown")

    def check():
        event_order.append("check")

    case = TestCase("example_test", check, tally=Tally(), teardown=teardown)
    case.run()
    assert event_order == ["check", "teardown"]  # AC-2.5

def test_test_case_tear_down_runs_on_failure():
    teardown_called = [False]

    def teardown():
        teardown_called[0] = True

    def failing_check():
        assert False  # This will fail

    case = TestCase("example_test", failing_check, tally=Tally(), teardown=teardown)
    case.run()
    assert teardown_called[0]  # AC-2.6

def test_failure_is_captured():
    tally = Tally()

    def failing_check():
        assert False  # This will fail

    case = TestCase("example_test", failing_check, tally=tally)
    case.run()
    assert tally.summary() == "1 run, 1 failed"  # AC-3.1

def test_test_suite_runs_multiple_cases():
    tally = Tally()

    def passing_check():
        pass

    case1 = TestCase("passing_test_1", passing_check, tally)
    case2 = TestCase("passing_test_2", passing_check, tally)
    suite = TestSuite([case1, case2])
    suite.run()
    
    assert tally.summary() == "2 run, 0 failed"  # AC-4.1

def test_test_suite_runs_empty_cases():
    tally = Tally()
    suite = TestSuite([])
    suite.run()
    
    assert tally.summary() == "0 run, 0 failed"  # Test for empty suite

def test_two_failing_cases_in_suite():
    tally = Tally()

    def failing_check():
        assert False  # This will fail

    case1 = TestCase("failing_test_1", failing_check, tally)
    case2 = TestCase("failing_test_2", failing_check, tally)
    suite = TestSuite([case1, case2])
    suite.run()
    
    assert tally.summary() == "2 run, 2 failed"  # Two tests run and both failed

def test_failing_case_with_teardown():
    teardown_called = [False]

    def teardown():
        teardown_called[0] = True

    def failing_check():
        assert False  # This will fail

    case = TestCase("example_test", failing_check, tally=Tally(), teardown=teardown)
    case.run()
    assert teardown_called[0]  # Teardown should run
    assert case.tally.summary() == "1 run, 1 failed"  # Tally should reflect one run, one failure