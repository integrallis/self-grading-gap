from solution import Tally, TestCase, TestSuite

def test_tally_initial_state():
    tally = Tally()
    # Expected: 0 runs and 0 failures
    assert tally.runs == 0
    assert tally.failures == 0

def test_tally_increment_runs():
    tally = Tally()
    tally.record_run()
    # Expected: 1 run and 0 failures
    assert tally.runs == 1
    assert tally.failures == 0

def test_tally_increment_failures():
    tally = Tally()
    tally.record_run()
    tally.record_failure()
    # Expected: 1 run and 1 failure
    assert tally.runs == 1
    assert tally.failures == 1

def test_tally_multiple_failures():
    tally = Tally()
    tally.record_run()
    tally.record_failure()
    tally.record_run()
    tally.record_failure()
    # Expected: 2 runs and 2 failures
    assert tally.runs == 2
    assert tally.failures == 2

def test_tally_summary_initial():
    tally = Tally()
    # Expected summary: "0 run, 0 failed"
    assert tally.summary() == "0 run, 0 failed"

def test_tally_summary_after_runs():
    tally = Tally()
    tally.record_run()
    tally.record_failure()
    # Expected summary: "1 run, 1 failed"
    assert tally.summary() == "1 run, 1 failed"

def test_test_case_initialization():
    test_case = TestCase("test_example")
    # Expected: test case name should be "test_example"
    assert test_case.name == "test_example"

def test_test_case_run_success():
    tally = Tally()
    test_case = TestCase("test_success")
    test_case.run(lambda: None, tally)  # Simulating a passing check
    # Expected: 1 run and 0 failures
    assert tally.runs == 1
    assert tally.failures == 0

def test_test_case_run_failure():
    tally = Tally()
    test_case = TestCase("test_failure")
    test_case.run(lambda: assert False, tally)  # Simulating a failing check
    # Expected: 1 run and 1 failure
    assert tally.runs == 1
    assert tally.failures == 1

def test_test_case_lifecycle():
    tally = Tally()
    test_case = TestCase("test_lifecycle")
    
    def check():
        assert True  # Simulating a passing check

    test_case.run(check, tally)
    # Expected: 1 run and 0 failures
    assert tally.runs == 1
    assert tally.failures == 0

def test_test_case_lifecycle_failure():
    tally = Tally()
    test_case = TestCase("test_lifecycle_failure")

    def check():
        assert False  # Simulating a failing check

    test_case.run(check, tally)
    # Expected: 1 run and 1 failure
    assert tally.runs == 1
    assert tally.failures == 1

def test_test_suite_run():
    tally = Tally()
    suite = TestSuite()
    test_case1 = TestCase("test_case_1")
    test_case2 = TestCase("test_case_2")

    def check1():
        assert True  # Simulating a passing check

    def check2():
        assert True  # Simulating a passing check

    suite.add(test_case1)
    suite.add(test_case2)
    
    test_case1.run(check1, tally)
    test_case2.run(check2, tally)
    
    # Expected: 2 runs and 0 failures
    assert tally.runs == 2
    assert tally.failures == 0

def test_test_suite_run_with_failures():
    tally = Tally()
    suite = TestSuite()
    test_case1 = TestCase("test_case_1")
    test_case2 = TestCase("test_case_2")

    def check1():
        assert True  # Simulating a passing check

    def check2():
        assert False  # Simulating a failing check

    suite.add(test_case1)
    suite.add(test_case2)

    test_case1.run(check1, tally)
    test_case2.run(check2, tally)
    
    # Expected: 2 runs and 1 failure
    assert tally.runs == 2
    assert tally.failures == 1