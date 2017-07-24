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

        if not test_result.wasSuccessful() and raise_error:
            raise Exception('Some tests did not pass')
        else:
            return test_result

