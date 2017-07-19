import unittest


class TestRunner:

    def __init__(self):
        self.loader = unittest.TestLoader()

    def runTests(self, test_cases=[], test_modules=[], raise_error=True):

        suite = unittest.TestSuite()

        for test_case in test_cases:
            suite.addTests(self.loader.loadTestsFromTestCase(test_case))

        for test_module in test_modules:
            suite.addTests(self.loader.loadTestsFromModule(test_module))

        test_result = unittest.TextTestRunner(verbosity=2).run(suite)
        failed_tests = test_result.failures

        if failed_tests and raise_error:
            raise Exception('Test failures: {}'.format(failed_tests))
        else:
            return test_result

