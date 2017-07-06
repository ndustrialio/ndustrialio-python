from ndustrialio.apiservices.tests.test_cases.test_api_client import TestAPIClient
from ndustrialio.workertools.test_runner import TestRunner

if __name__ == '__main__':
    test_runner = TestRunner()
    test_runner.runTestCases([TestAPIClient])