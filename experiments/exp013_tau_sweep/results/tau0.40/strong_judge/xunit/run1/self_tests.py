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
    # Two failing cases run under one tally show two failures.
    assert tally.runs == 2
    assert tally.failures == 2

def test_tally_summary_initial():
    tally = Tally()
    # A fresh tally reads "0 run, 0 failed".
    assert tally.summary() == "0 run, 0 failed"

def test_tally_summary_after_runs():
    tally = Tally()
    tally.record_run()
    tally.record_run()
    tally.record_failure()
    # After two starts and one failure it reads "2 run, 1 failed".
    assert tally.summary() == "2 run, 1 failed"

def test_test_case_initialization():
    def check_function():
        pass
    test_case = TestCase("test_check", check_function)
    # A test case is created with the name of the check it should exercise.
    assert test_case.name == "test_check"

def test_test_case_run_success():
    tally = Tally()
    
    def check_function():
        pass  # This check passes
    
    test_case = TestCase("test_check", check_function)
    test_case.run(tally)
    # Running a test case records the run in the supplied tally, which then reads "1 run, 0 failed".
    assert tally.runs == 1
    assert tally.failures == 0

def test_test_case_run_failure():
    tally = Tally()
    
    def check_function():
        assert False  # This check fails
    
    test_case = TestCase("test_check", check_function)
    test_case.run(tally)
    # An assertion failure inside a check is captured by the harness; the run completes and the tally reads "1 run, 1 failed".
    assert tally.runs == 1
    assert tally.failures == 1

def test_test_case_lifecycle():
    tally = Tally()
    
    class TestCaseWithLifecycle(TestCase):
        def set_up(self):
            self.setup_done = True
            
        def tear_down(self):
            self.teardown_done = True
        
        def check_function(self):
            assert self.setup_done  # Ensure setup ran
            assert not hasattr(self, 'teardown_done')  # Ensure teardown hasn't run yet
            
    test_case = TestCaseWithLifecycle("test_check_with_lifecycle", TestCaseWithLifecycle.check_function)
    test_case.run(tally)
    # Tear-down runs even when the check fails, and the failure is still tallied.
    assert tally.runs == 1
    assert tally.failures == 0
    assert hasattr(test_case, 'teardown_done')  # Ensure tear_down ran

def test_test_case_lifecycle_failure():
    tally = Tally()
    
    class TestCaseWithLifecycle(TestCase):
        def set_up(self):
            self.setup_done = True
            
        def tear_down(self):
            self.teardown_done = True
        
        def check_function(self):
            assert self.setup_done  # Ensure setup ran
            assert False  # This check fails
            
    test_case = TestCaseWithLifecycle("test_check_with_lifecycle", TestCaseWithLifecycle.check_function)
    test_case.run(tally)
    # Tear-down runs even when the check fails, and the failure is still tallied.
    assert tally.runs == 1
    assert tally.failures == 1
    assert hasattr(test_case, 'teardown_done')  # Ensure tear_down ran

def test_test_suite_run():
    tally = Tally()
    
    def check_function_pass():
        pass

    def check_function_fail():
        assert False  # This check fails
    
    test_case1 = TestCase("test_case_pass", check_function_pass)
    test_case2 = TestCase("test_case_fail", check_function_fail)
    suite = TestSuite(test_case1, test_case2)  # Accepting individual test cases
    suite.run(tally)
    # Two passing cases yield the summary "2 run, 0 failed".
    assert tally.runs == 2
    assert tally.failures == 1  # One case fails

    # The summary is "2 run, 1 failed".
    assert tally.summary() == "2 run, 1 failed"

def test_test_suite_run_with_pass_after_fail():
    tally = Tally()
    
    def check_function_fail():
        assert False  # This check fails

    def check_function_pass():
        pass  # This check passes
    
    test_case1 = TestCase("test_case_fail", check_function_fail)
    test_case2 = TestCase("test_case_pass", check_function_pass)
    suite = TestSuite(test_case1, test_case2)  # Accepting individual test cases
    suite.run(tally)
    # The tally should show that one case failed and one case passed.
    assert tally.runs == 2
    assert tally.failures == 1  # One case fails

    # The summary is "2 run, 1 failed".
    assert tally.summary() == "2 run, 1 failed"