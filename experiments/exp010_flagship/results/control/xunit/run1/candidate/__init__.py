class Tally:
    def __init__(self):
        self.runs = 0
        self.failures = 0

    def record_run(self):
        self.runs += 1

    def record_failure(self):
        self.failures += 1

    def summary(self):
        return f'{self.runs} run, {self.failures} failed'

class TestCase:
    def __init__(self, name):
        self.name = name

    def run(self, check, tally):
        try:
            check()
            tally.record_run()
        except AssertionError:
            tally.record_failure()

class TestSuite:
    def __init__(self):
        self.test_cases = []

    def add(self, test_case):
        self.test_cases.append(test_case)

    def run(self, tally):
        for test_case in self.test_cases:
            test_case.run(test_case.check_function, tally)  # This call is not valid anymore and should be corrected
