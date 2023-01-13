# Oded Ginat Dec 2022 Anzu

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

        def runTest(self):
            print("\n-------- TEST PLAN: {} --------".format(self.name.upper()))
            for idx, test in enumerate(self.tests):
                try:
                    instance = self.setup_method()
                except TypeError:
                    instance = self.setup_method(None)
                if hasattr(instance, self.method_to_test.__name__):
                    print(idx, "-\tTesting {}\n\t\t{}".format(self.method_to_test.__name__, test["input"]))
                    result = self.method_to_test(instance, *test["input"])
                    if "output" in test.keys():
                        print("\t\texpected:", test["output"], "got:", result)
                        self.assertEqual(result, test["output"])
                    elif "asserting_method" in test.keys():
                        print("\t\tchecking result", result)
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
            setattr(GlobalTester, "test_" + name, test_plan.runTest)
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
            try:
                test_dicts = func()
            except TypeError:
                test_dicts = func(None)
            for test in test_dicts:
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
