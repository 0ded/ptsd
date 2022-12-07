import unittest
from unittest import TestCase


class GlobalTester(TestCase):
    test_plans = []

    class TestPlan(TestCase):
        def __init__(self, test_name):
            super().__init__()
            self.name = test_name
            self.method_to_test = None
            self.setup_method = None
            self.tests = []

        def tie_method(self, method: callable):
            self.method_to_test = method

        def add_test(self, test: callable):
            self.tests.append(test)

        def set_setup(self, setup: callable):
            self.setup_method = setup

        def __str__(self):
            return self.name

        def test_main(self):
            for test in self.tests:
                print("TEST PLAN: ", test.name)
                instance = self.setup_method()
                if hasattr(instance, self.method_to_test.__name__):
                    print("Testing {}({})".format(self.method_to_test.__name__, test["input"]))
                    result = self.method_to_test(instance, *test["input"])
                    if "output" in test.keys():
                        print("expected:", test["output"], "got:", result)
                        self.assertEqual(result, test["output"])
                    elif "asserting_method" in test.keys():
                        print("checking result", result)
                        self.assertTrue(test["asserting_method"](result))

    @staticmethod
    def get_test(name):
        for plan in GlobalTester.test_plans:
            if plan.name == name:
                return plan
        return None

    @staticmethod
    def add_test(name):
        test_plan = GlobalTester.get_test(name)
        if not test_plan:
            test_plan = GlobalTester.TestPlan(name)
            GlobalTester.test_plans.append(test_plan)
        return test_plan

    class setup(staticmethod):
        def __init__(self, name):
            self.test_plan = GlobalTester.add_test(name)

        def __call__(self, func: callable):
            self.test_plan.set_setup(func)
            return staticmethod(func)

    class check(staticmethod):
        def __init__(self, name):
            self.test_plan = GlobalTester.add_test(name)

        def __call__(self, func: callable):
            for test in func():
                self.test_plan.add_test(test)

    class unit(staticmethod):
        def __init__(self, *names):
            self.local_test_plans = []
            for name in names:
                self.local_test_plans.append(GlobalTester.add_test(name))

        def __call__(self, func: callable):
            for test_plan in self.local_test_plans:
                test_plan.tie_method(func)
            return staticmethod(func)

    # def __call__(self):
    #     return [(str(test_plan), test_plan()) for test_plan in self.test_plans]

    def test_all(self):
        for test in GlobalTester.test_plans:
            test.test_main()


class ToTest:
    def __init__(self):
        self.c = 9

    @GlobalTester.unit("adder", "adder_mod")
    def adder(self, a: int, b: int):
        t = a + b + self.c
        self.c = 5
        return t

    @GlobalTester.unit("local")
    def local_changer(self, num):
        self.c = num

    class tests:
        @GlobalTester.setup("adder")
        def adder_setup() -> "ToTest":
            return ToTest()

        @GlobalTester.check("adder")
        def test_adder():
            return [{"input": [3, 5],
                     "output": 9+3+5},
                    {"input": [1, 1],
                     "asserting_method": lambda x: x == 1+1+9}]

        @GlobalTester.setup("adder_mod")
        def adder_setup() -> "ToTest":
            t = ToTest()
            t.c = 4
            return t

        @GlobalTester.check("adder_mod")
        def test_adder():
            return [{"input": [3, 5],
                     "output": 4 + 3 + 5},
                    {"input": [1, 1],
                     "asserting_method": lambda x: x == 1 + 1 }]


if __name__ == '__main__':
    unittest.main()
    GlobalTester()()
