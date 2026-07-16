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
    def __init__(self, name):
        self.name = name

    def run(self, tally):
        tally.record_run()
        # Simulate test result based on the name of the test
        if "failure" in self.name:
            tally.record_failure()

class TestSuite:
    def __init__(self):
        self.cases = []

    def add_case(self, case):
        self.cases.append(case)

    def run(self, tally):
        for case in self.cases:
            case.run(tally)
