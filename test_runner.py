from ndustrialio.apiservices.tests.unit_tests.test_api_client import TestAPIClient
from ndustrialio.workertools.test_runner import TestRunner

if __name__ == '__main__':
    test_runner = TestRunner()
    test_runner.runTestCases([TestAPIClient])