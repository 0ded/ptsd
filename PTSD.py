
class GlobalTester:
    class TestPlan:
        def __init__(self, testable: callable, arguments: list, outcome_test: callable):
            self.testable = testable
            self.arguments = arguments
            self.outcome_test = outcome_test

        def __call__(self):
            return self.outcome_test(self.testable(*self.arguments))

        def __str__(self):
            self.testable.__name__

    test_plans = []

    @staticmethod
    def static_test(so: callable):
        def inner():
            pass

    def __call__(self):
        return [(str(test_plan), test_plan()) for test_plan in self.test_plans]


class ToTest:
    @staticmethod
    def adder(a: int, b: int):
        return a + b

    class tests:
        @GlobalTester.static_test(super.adder)
        def test_adder(self):
            return


