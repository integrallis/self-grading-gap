from solution import Tally, TestCase, TestSuite

def test_tally_initialization():
    tally = Tally()
    assert tally.runs == 0  # AC-1.1: Fresh tally shows zero tests run
    assert tally.failures == 0  # AC-1.1: Fresh tally shows zero failures

def test_tally_increment_run():
    tally = Tally()
    tally.record_run()
    assert tally.runs == 1  # AC-1.2: Recording that a test started increments the run count by one

def test_tally_increment_failure():
    tally = Tally()
    tally.record_run()
    tally.record_failure()
    assert tally.failures == 1  # AC-1.3: Recording a failure increments the failure count by one

def test_tally_multiple_failures():
    tally = Tally()
    tally.record_run()
    tally.record_failure()
    tally.record_run()
    tally.record_failure()
    assert tally.failures == 2  # AC-1.3: Two failing cases should show two failures

def test_tally_summary():
    tally = Tally()
    assert tally.summary() == "0 run, 0 failed"  # AC-1.4: Fresh tally reads "0 run, 0 failed"
    tally.record_run()
    tally.record_failure()
    assert tally.summary() == "1 run, 1 failed"  # AC-1.4: After one start and one failure
    tally.record_run()
    assert tally.summary() == "2 run, 1 failed"  # AC-1.4: After two starts and one failure

def test_test_case_initialization():
    def dummy_check():
        pass
    test_case = TestCase("Dummy Test", dummy_check)
    assert test_case.name == "Dummy Test"  # AC-2.1: Test case exposes the name of the check

def test_test_case_run_success():
    tally = Tally()
    def passing_check():
        pass
    test_case = TestCase("Passing Test", passing_check)
    test_case.run(tally)
    assert tally.runs == 1  # AC-2.3: Tally should read "1 run, 0 failed" for a passing case
    assert tally.failures == 0

def test_test_case_run_failure():
    tally = Tally()
    def failing_check():
        assert False  # Force a failure
    test_case = TestCase("Failing Test", failing_check)
    test_case.run(tally)
    assert tally.runs == 1  # AC-3.1: Tally should read "1 run, 1 failed"
    assert tally.failures == 1

def test_test_case_setup_teardown():
    tally = Tally()
    setup_ran = False
    teardown_ran = False

    def setup():
        nonlocal setup_ran
        setup_ran = True

    def teardown():
        nonlocal teardown_ran
        teardown_ran = True

    def check():
        pass

    test_case = TestCase("Test with Setup and Teardown", check, setup, teardown)
    test_case.run(tally)
    assert setup_ran  # AC-2.4: Setup should run before the check
    assert teardown_ran  # AC-2.5: Teardown should run after the check

def test_test_case_teardown_on_failure():
    tally = Tally()
    setup_ran = False
    teardown_ran = False

    def setup():
        nonlocal setup_ran
        setup_ran = True

    def teardown():
        nonlocal teardown_ran
        teardown_ran = True

    def failing_check():
        assert False  # Force a failure

    test_case = TestCase("Failing Test with Setup and Teardown", failing_check, setup, teardown)
    test_case.run(tally)
    assert setup_ran  # AC-2.4: Setup should run before the check
    assert teardown_ran  # AC-2.5: Teardown should run after the check

def test_test_suite_run():
    tally = Tally()

    def passing_check():
        pass

    def failing_check():
        assert False  # Force a failure

    test_case1 = TestCase("Passing Test", passing_check)
    test_case2 = TestCase("Failing Test", failing_check)

    suite = TestSuite([test_case1, test_case2])
    suite.run(tally)

    assert tally.runs == 2  # AC-4.1: Two tests run in the suite
    assert tally.failures == 1  # AC-4.1: One test fails in the suite