# PTSD - Python Test Suite Decorator

[![Python application](https://github.com/0ded/ptsd/actions/workflows/python-app.yml/badge.svg?event=check_run)](https://github.com/0ded/ptsd/actions/workflows/python-app.yml)

A library for writing and runnint basic unit tests in python. 

Tag the function you wish to test with `@GlobalTester.unit("tag name")`

Connect it to a test function using `@GlobalTester.check("tag name")`


## EXAMPLE 

```
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
                     "output": 9 + 3 + 5},
                    {"input": [1, 1],
                     "asserting_method": lambda x: x == 1 + 1 + 9}]

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
                     "asserting_method": lambda x: x == 1 + 1}]


if __name__ == '__main__':
    unittest.main()
    # GlobalTester()()
```
