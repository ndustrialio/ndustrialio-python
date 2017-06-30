import unittest


class TestRunner:

    def __init__(self):
        self.loader = unittest.TestLoader()

    def runTestCases(self, test_cases=None, raise_error=True):

        suite = unittest.TestSuite()

        for test_case in test_cases:
            suite.addTests(self.loader.loadTestsFromTestCase(test_case))

        test_result = unittest.TextTestRunner(verbosity=2).run(suite)
        failed_tests = test_result.failures

        if failed_tests and raise_error:
            raise Exception('Test failures: {}'.format(failed_tests))
        else:
            return test_result