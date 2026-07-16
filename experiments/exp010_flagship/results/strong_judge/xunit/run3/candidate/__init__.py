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
        tally.record_run()  # Record the run first
        if self.setup:
            self.setup()
        try:
            self.check()
        except AssertionError:
            tally.record_failure()
        finally:
            if self.teardown:
                self.teardown()

class TestSuite:
    def __init__(self, cases):
        self.cases = cases

    def run(self, tally):
        for case in self.cases:
            case.run(tally)