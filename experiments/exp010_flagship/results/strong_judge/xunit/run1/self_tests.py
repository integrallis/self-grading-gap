from solution import Tally, TestCase, TestSuite

def test_tally_initialization():
    tally = Tally()
    # Fresh tally shows zero tests run and zero failures.
    assert tally.runs == 0
    assert tally.failures == 0

def test_tally_record_run():
    tally = Tally()
    tally.record_run()
    # Recording that a test started increments the run count by one.
    assert tally.runs == 1
    assert tally.failures == 0

def test_tally_record_failure():
    tally = Tally()
    tally.record_run()
    tally.record_failure()
    # Recording a failure increments the failure count by one.
    assert tally.runs == 1
    assert tally.failures == 1

def test_tally_multiple_failures():
    tally = Tally()
    tally.record_run()
    tally.record_failure()
    tally.record_run()
    tally.record_failure()
    # Two failing cases yield two failures.
    assert tally.runs == 2
    assert tally.failures == 2

def test_tally_summary_initialization():
    tally = Tally()
    # A fresh tally reads "0 run, 0 failed".
    assert tally.summary() == "0 run, 0 failed"

def test_tally_summary_after_runs():
    tally = Tally()
    tally.record_run()
    tally.record_failure()
    # After one start and one failure, it reads "1 run, 1 failed".
    assert tally.summary() == "1 run, 1 failed"

def test_tally_summary_after_multiple_runs():
    tally = Tally()
    tally.record_run()
    tally.record_run()
    tally.record_failure()
    # After two starts and one failure it reads "2 run, 1 failed".
    assert tally.summary() == "2 run, 1 failed"

def test_test_case_initialization():
    def check():
        pass
    case = TestCase("Test check", check)
    # A test case is created with the name of the check it should exercise.
    assert case.name == "Test check"

def test_test_case_run_success():
    tally = Tally()
    def check():
        pass  # This check should pass
    case = TestCase("Passing test", check)
    case.run(tally)
    # Running a test case records the run in the supplied tally.
    assert tally.runs == 1
    assert tally.failures == 0

def test_test_case_run_failure():
    tally = Tally()
    def check():
        assert False  # This check should fail
    case = TestCase("Failing test", check)
    case.run(tally)
    # Running a test case records the run in the supplied tally and captures the failure.
    assert tally.runs == 1
    assert tally.failures == 1

def test_test_case_setup_teardown_order():
    tally = Tally()
    event_log = []

    def setup():
        event_log.append("setup")

    def teardown():
        event_log.append("teardown")

    def check():
        event_log.append("check")

    case = TestCase("Test with setup, check, and teardown", check, setup, teardown)
    case.run(tally)

    # Check the order of events.
    assert event_log == ["setup", "check", "teardown"]
    # Tally remains accurate.
    assert tally.runs == 1
    assert tally.failures == 0

def test_test_case_run_failure_with_teardown():
    tally = Tally()
    event_log = []

    def setup():
        event_log.append("setup")

    def teardown():
        event_log.append("teardown")

    def check():
        assert False  # This check should fail

    case = TestCase("Failing test with teardown", check, setup, teardown)
    case.run(tally)

    # Check that the teardown still runs after the failing check.
    assert event_log == ["setup", "teardown"]
    # Tally should reflect the failure.
    assert tally.runs == 1
    assert tally.failures == 1

def test_suite_run_multiple_cases():
    tally = Tally()
    def check_pass():
        pass  # This check should pass

    def check_fail():
        assert False  # This check should fail

    case1 = TestCase("Passing test", check_pass)
    case2 = TestCase("Failing test", check_fail)
    suite = TestSuite([case1, case2])
    suite.run(tally)

    # Two cases yield the summary "2 run, 1 failed".
    assert tally.runs == 2
    assert tally.failures == 1

def test_suite_run_two_passing_cases():
    tally = Tally()
    def check_pass1():
        pass  # This check should pass

    def check_pass2():
        pass  # This check should pass

    case1 = TestCase("Passing test 1", check_pass1)
    case2 = TestCase("Passing test 2", check_pass2)
    suite = TestSuite([case1, case2])
    suite.run(tally)

    # Two passing cases yield the summary "2 run, 0 failed".
    assert tally.runs == 2
    assert tally.failures == 0
    assert tally.summary() == "2 run, 0 failed"

def test_suite_run_empty_cases():
    tally = Tally()
    suite = TestSuite([])
    suite.run(tally)

    # An empty suite should leave the tally at zero.
    assert tally.runs == 0
    assert tally.failures == 0
    assert tally.summary() == "0 run, 0 failed"

def test_suite_run_three_cases():
    tally = Tally()

    def check_pass():
        pass  # This check should pass

    def check_fail():
        assert False  # This check should fail

    case1 = TestCase("Passing test", check_pass)
    case2 = TestCase("Failing test", check_fail)
    case3 = TestCase("Another passing test", check_pass)
    suite = TestSuite([case1, case2, case3])
    suite.run(tally)

    # Three cases with one failing case yield "3 run, 1 failed".
    assert tally.runs == 3
    assert tally.failures == 1