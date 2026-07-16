from solution import Tally, TestCase, TestSuite

def test_tally_initial_state():
    tally = Tally()
    # fresh tally shows zero tests run and zero failures
    assert tally.get_runs() == 0
    assert tally.get_failures() == 0

def test_tally_record_run():
    tally = Tally()
    tally.record_run()
    # recording that a test started increments the run count by one
    assert tally.get_runs() == 1
    assert tally.get_failures() == 0

def test_tally_record_failure():
    tally = Tally()
    tally.record_run()
    tally.record_failure()
    # recording a failure increments the failure count by one
    assert tally.get_runs() == 1
    assert tally.get_failures() == 1

def test_tally_multiple_failures():
    tally = Tally()
    tally.record_run()
    tally.record_failure()
    tally.record_run()
    tally.record_failure()
    # two failing cases run under one tally show two failures
    assert tally.get_runs() == 2
    assert tally.get_failures() == 2

def test_tally_summary_initial():
    tally = Tally()
    # fresh tally reads "0 run, 0 failed"
    assert tally.summary() == "0 run, 0 failed"

def test_tally_summary_after_runs():
    tally = Tally()
    tally.record_run()
    tally.record_run()
    tally.record_failure()
    # after two starts and one failure it reads "2 run, 1 failed"
    assert tally.summary() == "2 run, 1 failed"

def test_test_case_creation():
    case = TestCase("example_check", lambda: None)
    # test case is created with the name of the check it should exercise
    assert case.get_name() == "example_check"

def test_test_case_run_success():
    tally = Tally()
    case = TestCase("example_check", lambda: None)  # Passing check
    case.run(tally)
    # running a test case records the run in the supplied tally
    assert tally.get_runs() == 1
    assert tally.get_failures() == 0

def test_test_case_run_failure():
    tally = Tally()
    case = TestCase("example_check", lambda: (_ for _ in ()).throw(AssertionError()))  # Failing check
    case.run(tally)
    # running a test case records the run in the supplied tally and captures the failure
    assert tally.get_runs() == 1
    assert tally.get_failures() == 1

def test_test_case_run_setup_and_teardown():
    tally = Tally()
    events = []

    def setup():
        events.append("setup")
    
    def teardown():
        events.append("teardown")
    
    def check():
        events.append("check")  # Passing check

    case = TestCase("example_check", check, setup, teardown)
    case.run(tally)
    # setup runs before the check itself, and teardown runs after the check
    assert events == ["setup", "check", "teardown"]

def test_test_case_run_teardown_on_failure():
    tally = Tally()
    events = []

    def setup():
        events.append("setup")
    
    def teardown():
        events.append("teardown")

    def check():
        assert False  # Failing check

    case = TestCase("example_check", check, setup, teardown)
    case.run(tally)
    # teardown runs even when the check fails
    assert events == ["setup", "teardown"]
    assert tally.get_runs() == 1
    assert tally.get_failures() == 1

def test_test_suite_run_cases():
    tally = Tally()
    case1 = TestCase("passing_case", lambda: None)  # Passing check
    case2 = TestCase("failing_case", lambda: (_ for _ in ()).throw(AssertionError()))  # Failing check
    suite = TestSuite([case1, case2])
    suite.run(tally)
    # two cases yield the summary "2 run, 1 failed"
    assert tally.get_runs() == 2
    assert tally.get_failures() == 1

def test_test_suite_run_two_passing_cases():
    tally = Tally()
    case1 = TestCase("passing_case_1", lambda: None)  # Passing check
    case2 = TestCase("passing_case_2", lambda: None)  # Passing check
    suite = TestSuite([case1, case2])
    suite.run(tally)
    # two passing cases yield the summary "2 run, 0 failed"
    assert tally.get_runs() == 2
    assert tally.get_failures() == 0

def test_test_suite_run_empty():
    tally = Tally()
    suite = TestSuite([])
    suite.run(tally)
    # empty suite should leave the tally at "0 run, 0 failed"
    assert tally.get_runs() == 0
    assert tally.get_failures() == 0