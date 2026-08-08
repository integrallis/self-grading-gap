from solution import Tally, TestCase, Suite

def test_tally_initialization():
    tally = Tally()
    # Fresh tally should show 0 runs and 0 failures
    assert tally.runs == 0
    assert tally.failures == 0
    # Summary should read "0 run, 0 failed"
    assert tally.summary() == "0 run, 0 failed"

def test_tally_increment_run():
    tally = Tally()
    tally.record_run()
    # After one run, tally should show 1 run and 0 failures
    assert tally.runs == 1
    assert tally.failures == 0

def test_tally_increment_failure():
    tally = Tally()
    tally.record_run()
    tally.record_failure()
    # After one run and one failure, tally should show 1 run and 1 failure
    assert tally.runs == 1
    assert tally.failures == 1

def test_tally_summary():
    tally = Tally()
    tally.record_run()
    tally.record_failure()
    tally.record_run()
    # After two runs with one failure, summary should be "2 run, 1 failed"
    assert tally.summary() == "2 run, 1 failed"

def test_tally_multiple_failures():
    tally = Tally()
    tally.record_run()
    tally.record_failure()
    tally.record_run()
    tally.record_failure()
    # After two runs with two failures, tally should show 2 runs and 2 failures
    assert tally.runs == 2
    assert tally.failures == 2

def test_test_case_initialization():
    def sample_check():
        pass
    test_case = TestCase("Sample Check", sample_check)
    # Test case should expose its name correctly
    assert test_case.name == "Sample Check"

def test_test_case_run_success():
    tally = Tally()
    
    def passing_check():
        return "check executed"  # Side effect to verify execution
    
    test_case = TestCase("Passing Check", passing_check)
    test_case.run(tally)
    # After running a passing case, tally should show 1 run and 0 failures
    assert tally.runs == 1
    assert tally.failures == 0

def test_test_case_run_failure():
    tally = Tally()
    
    def failing_check():
        assert False  # This check fails
    
    test_case = TestCase("Failing Check", failing_check)
    test_case.run(tally)
    # After running a failing case, tally should show 1 run and 1 failure
    assert tally.runs == 1
    assert tally.failures == 1

def test_test_case_setup_teardown():
    tally = Tally()
    lifecycle_events = []
    
    def setup():
        lifecycle_events.append("setup")

    def teardown():
        lifecycle_events.append("teardown")

    def check():
        lifecycle_events.append("check")  # Side effect to verify execution

    test_case = TestCase("Setup Teardown Check", check, setup, teardown)
    test_case.run(tally)
    # Setup and teardown should both be called
    assert lifecycle_events == ["setup", "check", "teardown"]
    # Tally should show 1 run and 0 failures
    assert tally.runs == 1
    assert tally.failures == 0

def test_test_case_run_failure_teardown():
    tally = Tally()
    lifecycle_events = []
    
    def setup():
        lifecycle_events.append("setup")

    def teardown():
        lifecycle_events.append("teardown")

    def failing_check():
        assert False  # This check fails

    test_case = TestCase("Failing Check with Teardown", failing_check, setup, teardown)
    test_case.run(tally)
    # Lifecycle should include both setup and teardown even after failure
    assert lifecycle_events == ["setup", "teardown"]
    # Tally should show 1 run and 1 failure
    assert tally.runs == 1
    assert tally.failures == 1

def test_suite_with_multiple_cases():
    tally = Tally()

    def passing_check_1():
        pass

    def passing_check_2():
        pass

    test_case_1 = TestCase("Passing Check 1", passing_check_1)
    test_case_2 = TestCase("Passing Check 2", passing_check_2)
    
    suite = Suite([test_case_1, test_case_2])
    suite.run(tally)
    # After running two passing cases, tally should show 2 runs and 0 failures
    assert tally.runs == 2
    assert tally.failures == 0
    # Summary should read "2 run, 0 failed"
    assert tally.summary() == "2 run, 0 failed"

def test_suite_with_failing_and_passing_case():
    tally = Tally()

    def failing_check():
        assert False  # This check fails

    def passing_check():
        pass

    test_case_1 = TestCase("Failing Check", failing_check)
    test_case_2 = TestCase("Passing Check", passing_check)
    
    suite = Suite([test_case_1, test_case_2])
    suite.run(tally)
    # After running one failing case and one passing case, tally should show 2 runs and 1 failure
    assert tally.runs == 2
    assert tally.failures == 1
    # Summary should read "2 run, 1 failed"
    assert tally.summary() == "2 run, 1 failed"

def test_empty_suite():
    tally = Tally()
    suite = Suite([])
    suite.run(tally)
    # After running an empty suite, tally should show 0 runs and 0 failures
    assert tally.runs == 0
    assert tally.failures == 0
    # Summary should read "0 run, 0 failed"
    assert tally.summary() == "0 run, 0 failed"