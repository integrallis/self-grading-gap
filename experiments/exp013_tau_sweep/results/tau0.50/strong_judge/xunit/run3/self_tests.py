from solution import Tally, TestCase, TestSuite

def test_tally_initial_state():
    tally = Tally()
    # fresh tally shows zero tests run and zero failures
    assert tally.runs == 0
    assert tally.failures == 0

def test_tally_increment_runs():
    tally = Tally()
    tally.record_run()
    # recording that a test started increments the run count by one
    assert tally.runs == 1
    assert tally.failures == 0

def test_tally_increment_failures():
    tally = Tally()
    tally.record_run()
    tally.record_failure()
    # recording a failure increments the failure count by one
    assert tally.runs == 1
    assert tally.failures == 1
    tally.record_failure()
    # two failing cases run under one tally show two failures
    assert tally.failures == 2

def test_tally_summary():
    tally = Tally()
    assert tally.summary() == "0 run, 0 failed"  # fresh tally reads "0 run, 0 failed"
    tally.record_run()
    assert tally.summary() == "1 run, 0 failed"  # after one run, should read "1 run, 0 failed"
    tally.record_failure()
    assert tally.summary() == "1 run, 1 failed"  # after one failure should read "1 run, 1 failed"
    tally.record_run()
    tally.record_failure()
    assert tally.summary() == "2 run, 2 failed"  # after two runs and two failures should read "2 run, 2 failed"
    tally.record_run()
    assert tally.summary() == "3 run, 2 failed"  # after three runs and two failures should read "3 run, 2 failed"

def test_test_case_initialization():
    def check_function():
        pass
    case = TestCase("test_check", check_function)
    # a test case is created with the name of the check it should exercise
    assert case.name == "test_check"

def test_test_case_run_success():
    tally = Tally()
    def check_function():
        pass  # passing check
    case = TestCase("test_check", check_function)
    case.run(tally)
    # running a test case records the run in the supplied tally
    assert tally.runs == 1
    assert tally.failures == 0
    assert tally.summary() == "1 run, 0 failed"  # should read "1 run, 0 failed"

def test_test_case_run_failure():
    tally = Tally()
    def check_function():
        assert False  # failing check
    case = TestCase("test_check", check_function)
    case.run(tally)
    # running a test case records the run in the supplied tally
    assert tally.runs == 1
    assert tally.failures == 1  # should count the failure
    assert tally.summary() == "1 run, 1 failed"  # should read "1 run, 1 failed"

def test_test_case_setup_and_teardown():
    tally = Tally()
    events = []
    
    def setup():
        events.append("setup")
    
    def teardown():
        events.append("teardown")
    
    def check_function():
        events.append("check")  # this will be called during the test
    
    case = TestCase("test_check", check_function, setup, teardown)
    case.run(tally)
    assert events == ["setup", "check", "teardown"]  # verify the order of events

def test_test_case_teardown_on_failure():
    tally = Tally()
    events = []
    
    def setup():
        events.append("setup")
    
    def teardown():
        events.append("teardown")
    
    def check_function():
        assert False  # failing check
    
    case = TestCase("test_check", check_function, setup, teardown)
    case.run(tally)
    assert tally.runs == 1
    assert tally.failures == 1  # should count the failure
    assert events == ["setup", "teardown"]  # teardown should run even when the check fails

def test_test_suite_run():
    tally = Tally()
    
    def check_function_pass():
        assert True  # passing check

    def check_function_fail():
        assert False  # failing check

    case1 = TestCase("test_check_pass", check_function_pass)
    case2 = TestCase("test_check_fail", check_function_fail)
    suite = TestSuite([case1, case2])
    suite.run(tally)
    
    assert tally.runs == 2  # two cases run
    assert tally.failures == 1  # one failure should count
    assert tally.summary() == "2 run, 1 failed"  # summary after running the suite

def test_test_suite_run_empty():
    tally = Tally()
    suite = TestSuite([])  # empty suite
    suite.run(tally)
    
    assert tally.runs == 0  # no cases should result in zero runs
    assert tally.failures == 0  # no cases should result in zero failures
    assert tally.summary() == "0 run, 0 failed"  # summary should reflect no runs or failures

def test_test_suite_continue_after_failure():
    tally = Tally()

    def check_function_fail():
        assert False  # failing check

    def check_function_pass():
        assert True  # passing check

    case1 = TestCase("test_check_fail", check_function_fail)
    case2 = TestCase("test_check_pass", check_function_pass)
    suite = TestSuite([case1, case2])
    suite.run(tally)

    assert tally.runs == 2  # both cases should run
    assert tally.failures == 1  # only the first fails
    assert tally.summary() == "2 run, 1 failed"  # summary should reflect the results

def test_test_suite_two_failing_cases():
    tally = Tally()

    def check_function_fail_1():
        assert False  # first failing check

    def check_function_fail_2():
        assert False  # second failing check

    case1 = TestCase("test_check_fail_1", check_function_fail_1)
    case2 = TestCase("test_check_fail_2", check_function_fail_2)
    suite = TestSuite([case1, case2])
    suite.run(tally)

    assert tally.runs == 2  # two cases run
    assert tally.failures == 2  # two failures should count
    assert tally.summary() == "2 run, 2 failed"  # summary after running the suite

def test_test_suite_two_passing_cases():
    tally = Tally()

    def check_function_pass_1():
        assert True  # first passing check

    def check_function_pass_2():
        assert True  # second passing check

    case1 = TestCase("test_check_pass_1", check_function_pass_1)
    case2 = TestCase("test_check_pass_2", check_function_pass_2)
    suite = TestSuite([case1, case2])
    suite.run(tally)

    assert tally.runs == 2  # two cases run
    assert tally.failures == 0  # no failures should count
    assert tally.summary() == "2 run, 0 failed"  # summary after running the suite