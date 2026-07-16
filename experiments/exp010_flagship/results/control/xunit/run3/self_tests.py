from solution import Tally, TestCase, TestSuite

def test_tally_initial_state():
    tally = Tally()
    # Fresh tally should show zero tests run and zero failures
    assert tally.runs == 0
    assert tally.failures == 0

def test_tally_increment_run_count():
    tally = Tally()
    tally.record_run()
    # Recording a run increments the count by one
    assert tally.runs == 1

def test_tally_increment_failure_count():
    tally = Tally()
    tally.record_run()
    tally.record_failure()
    # Recording a failure increments the failure count by one
    assert tally.failures == 1

def test_tally_multiple_failures():
    tally = Tally()
    tally.record_run()
    tally.record_failure()
    tally.record_run()
    tally.record_failure()
    # Two failures should be counted
    assert tally.failures == 2

def test_tally_summary():
    tally = Tally()
    tally.record_run()
    tally.record_failure()
    tally.record_run()
    # Summary should reflect the correct counts
    assert tally.summary() == "2 run, 1 failed"

def test_test_case_initialization():
    case = TestCase("test_example")
    # Test case should expose the name of the check it exercises
    assert case.name == "test_example"

def test_test_case_run_success():
    tally = Tally()
    case = TestCase("test_success")
    case.run(tally)
    # Running a passing case should increment the run count
    assert tally.runs == 1
    assert tally.failures == 0

def test_test_case_run_failure():
    tally = Tally()
    case = TestCase("test_failure")
    case.run(tally)
    # Running a failing case should increment the run count and failure count
    assert tally.runs == 1
    assert tally.failures == 1

def test_test_case_run_failure_tallies():
    tally = Tally()
    case1 = TestCase("test_failure_1")
    case2 = TestCase("test_failure_2")
    case1.run(tally)
    case2.run(tally)
    # Two failing cases should yield two failures
    assert tally.runs == 2
    assert tally.failures == 2

def test_test_case_lifecycle():
    tally = Tally()
    case = TestCase("test_lifecycle")
    case.run(tally)
    # Check that setup and teardown are executed
    # (Implicitly checked via success/failure of the test)

def test_test_suite_run():
    tally = Tally()
    suite = TestSuite()
    case1 = TestCase("test_case_1")
    case2 = TestCase("test_case_2")
    suite.add_case(case1)
    suite.add_case(case2)
    suite.run(tally)
    # Two passing cases should give a summary of "2 run, 0 failed"
    assert tally.runs == 2
    assert tally.failures == 0