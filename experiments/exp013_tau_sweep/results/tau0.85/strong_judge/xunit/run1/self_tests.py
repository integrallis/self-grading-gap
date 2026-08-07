from solution import Tally, TestCase, TestSuite

def test_tally_initial_state():
    tally = Tally()
    # Fresh tally shows zero tests run and zero failures
    assert tally.run_count == 0
    assert tally.failure_count == 0
    assert tally.summary() == "0 run, 0 failed"

def test_tally_record_run():
    tally = Tally()
    tally.record_run()
    # Recording that a test started increments the run count by one
    assert tally.run_count == 1
    assert tally.failure_count == 0
    assert tally.summary() == "1 run, 0 failed"

def test_tally_record_failure():
    tally = Tally()
    tally.record_run()
    tally.record_failure()
    # Recording a failure increments the failure count by one
    assert tally.run_count == 1
    assert tally.failure_count == 1
    assert tally.summary() == "1 run, 1 failed"

def test_tally_multiple_failures():
    tally = Tally()
    tally.record_run()
    tally.record_failure()
    tally.record_run()
    tally.record_failure()
    # Two failing cases run under one tally show two failures
    assert tally.run_count == 2
    assert tally.failure_count == 2
    assert tally.summary() == "2 run, 2 failed"

def test_tally_summary_after_runs():
    tally = Tally()
    tally.record_run()
    tally.record_failure()
    tally.record_run()
    # After two starts and one failure it reads "2 run, 1 failed"
    assert tally.summary() == "2 run, 1 failed"

def test_test_case_exposes_name():
    case = TestCase("Test example")
    # A test case is created with the name of the check it should exercise
    assert case.name == "Test example"

def test_test_case_runs_check():
    tally = Tally()
    check_invoked = [False]

    def check():
        check_invoked[0] = True

    case = TestCase("Test example", check=check)
    case.run(tally)
    # Running a test case invokes the named check
    assert check_invoked[0] is True

def test_test_case_records_run():
    tally = Tally()
    check_invoked = [False]

    def check():
        check_invoked[0] = True

    case = TestCase("Passing test", check=check)
    case.run(tally)
    # Running a test case records the run in the supplied tally
    assert tally.run_count == 1
    assert tally.failure_count == 0
    assert check_invoked[0] is True
    assert tally.summary() == "1 run, 0 failed"

def test_test_case_runs_setup():
    events = []

    def setup():
        events.append("setup")

    def check():
        events.append("check")

    case = TestCase("Test with setup", setup=setup, check=check)
    case.run(Tally())
    # A case's set-up step runs before the check itself
    assert events == ["setup", "check"]

def test_test_case_runs_teardown():
    events = []

    def teardown():
        events.append("teardown")

    def check():
        events.append("check")

    case = TestCase("Test with teardown", teardown=teardown, check=check)
    case.run(Tally())
    # A case's tear-down step runs after the check itself
    assert events == ["check", "teardown"]

def test_test_case_teardown_on_failure():
    events = []

    def teardown():
        events.append("teardown")

    def check_fail():
        events.append("check")
        assert False  # This will fail

    case = TestCase("Failing test", check=check_fail, teardown=teardown)
    tally = Tally()
    case.run(tally)
    # Tear-down runs even when the check fails
    assert events == ["check", "teardown"]
    assert tally.run_count == 1
    assert tally.failure_count == 1
    assert tally.summary() == "1 run, 1 failed"

def test_test_case_failing_check_summary():
    tally = Tally()
    
    def check_fail():
        assert False  # This will fail

    case = TestCase("Failing test", check=check_fail)
    case.run(tally)
    # The tally's required rendered result is "1 run, 1 failed"
    assert tally.summary() == "1 run, 1 failed"

def test_test_suite_runs_cases():
    tally = Tally()
    suite = TestSuite()
    check1_invoked = [False]
    check2_invoked = [False]

    def check1():
        check1_invoked[0] = True

    def check2():
        check2_invoked[0] = True

    case1 = TestCase("Passing test 1", check=check1)
    case2 = TestCase("Passing test 2", check=check2)
    suite.add_case(case1)
    suite.add_case(case2)
    suite.run(tally)
    
    # Two passing cases yield the summary "2 run, 0 failed"
    assert tally.run_count == 2
    assert tally.failure_count == 0
    assert check1_invoked[0] is True
    assert check2_invoked[0] is True
    assert tally.summary() == "2 run, 0 failed"

def test_test_suite_failing_then_passing_case():
    tally = Tally()
    suite = TestSuite()
    
    def check_fail():
        assert False  # This will fail

    def check_pass():
        pass  # This will pass

    case1 = TestCase("Failing test", check=check_fail)
    case2 = TestCase("Passing test", check=check_pass)
    
    suite.add_case(case1)
    suite.add_case(case2)
    suite.run(tally)
    
    # The suite runs both cases, tallying the failure from the first and the success from the second
    assert tally.run_count == 2
    assert tally.failure_count == 1
    assert tally.summary() == "2 run, 1 failed"

def test_empty_suite():
    tally = Tally()
    suite = TestSuite()
    suite.run(tally)
    # An empty suite leaves the tally at "0 run, 0 failed"
    assert tally.run_count == 0
    assert tally.failure_count == 0
    assert tally.summary() == "0 run, 0 failed"