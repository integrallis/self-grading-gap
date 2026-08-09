class Tally:
    def __init__(self):
        self.runs = 0
        self.failures = 0

    def record_run(self):
        self.runs += 1

    def record_failure(self):
        self.failures += 1

    def summary(self):
        return f"{self.runs} run, {self.failures} failed"

class TestCase:
    def __init__(self, name, check, setup=None, teardown=None):
        self.name = name
        self.check = check
        self.setup = setup
        self.teardown = teardown

    def run(self, tally):
        if self.setup:
            self.setup()
        tally.record_run()
        try:
            self.check()
        except:
            tally.record_failure()
        finally:
            if self.teardown:
                self.teardown()

class Suite:
    def __init__(self, test_cases):
        self.test_cases = test_cases

    def run(self, tally):
        for test_case in self.test_cases:
            test_case.run(tally)