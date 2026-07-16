from solution import Tally, TestCase, TestSuite

def test_tally_initialization():
    tally = Tally()
    # A fresh tally shows zero tests run and zero failures.
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
    tally.record_run()  # First test run
    tally.record_failure()
    # Recording a failure increments the failure count by one.
    assert tally.runs == 1
    assert tally.failures == 1

def test_tally_multiple_failures():
    tally = Tally()
    tally.record_run()  # First test run
    tally.record_failure()
    tally.record_run()  # Second test run
    tally.record_failure()
    # Two failing cases run under one tally show two failures.
    assert tally.runs == 2
    assert tally.failures == 2

def test_tally_summary():
    tally = Tally()
    assert tally.summary() == "0 run, 0 failed"  # Fresh tally
    tally.record_run()
    assert tally.summary() == "1 run, 0 failed"  # After one run
    tally.record_failure()
    assert tally.summary() == "1 run, 1 failed"  # After one failure
    tally.record_run()
    assert tally.summary() == "2 run, 1 failed"  # After two runs, one failure

def test_test_case_initialization():
    def dummy_check():
        pass

    case = TestCase("Dummy Test", dummy_check)
    # A test case is created with the name of the check it should exercise.
    assert case.name == "Dummy Test"

def test_test_case_run_success():
    tally = Tally()
    events = []

    def passing_check():
        events.append("check")

    case = TestCase("Passing Test", passing_check)
    case.run(tally)
    # Running a test case records the run in the supplied tally.
    assert tally.runs == 1
    assert tally.failures == 0  # Case passed
    assert events == ["check"]  # Check was invoked
    assert tally.summary() == "1 run, 0 failed"  # Summary check

def test_test_case_run_failure():
    tally = Tally()
    def failing_check():
        assert False  # Intentional failure for the test

    case = TestCase("Failing Test", failing_check)
    case.run(tally)
    # Running a test case records the run and failure in the supplied tally.
    assert tally.runs == 1
    assert tally.failures == 1  # Case failed

def test_test_case_lifecycle():
    tally = Tally()
    events = []

    def setup():
        events.append("setup")

    def teardown():
        events.append("teardown")

    def check():
        events.append("check")

    case = TestCase("Check with Lifecycle", check, setup, teardown)
    case.run(tally)

    # Check if setup and teardown were called in the correct order
    assert events == ["setup", "check", "teardown"]
    # Tally should report the test run successfully
    assert tally.runs == 1
    assert tally.failures == 0

def test_test_case_lifecycle_failure():
    tally = Tally()
    events = []

    def setup():
        events.append("setup")

    def teardown():
        events.append("teardown")

    def check():
        assert False  # Intentional failure for the test

    case = TestCase("Failing Check with Lifecycle", check, setup, teardown)
    case.run(tally)

    # Check if setup and teardown were called in the correct order
    assert events == ["setup", "teardown"]  # Correct order after failure
    # Tally should report the test run with failure
    assert tally.runs == 1
    assert tally.failures == 1

def test_test_suite_run():
    tally = Tally()
    
    def passing_check():
        pass
    
    case1 = TestCase("Passing Test 1", passing_check)
    case2 = TestCase("Passing Test 2", passing_check)

    suite = TestSuite([case1, case2])
    suite.run(tally)

    # Suite should report the total runs and failures
    assert tally.runs == 2  # 2 passing cases
    assert tally.failures == 0  # No failures

def test_test_suite_run_with_failure():
    tally = Tally()
    
    def passing_check():
        pass
    
    def failing_check():
        assert False  # Intentional failure for the test

    case1 = TestCase("Passing Test 1", passing_check)
    case2 = TestCase("Failing Test 2", failing_check)

    suite = TestSuite([case1, case2])
    suite.run(tally)

    # Suite should report the total runs and failures
    assert tally.runs == 2  # 1 passing + 1 failing
    assert tally.failures == 1  # Only 1 failure

def test_empty_suite():
    tally = Tally()
    suite = TestSuite([])
    suite.run(tally)

    # Suite should report zero runs and failures
    assert tally.runs == 0
    assert tally.failures == 0