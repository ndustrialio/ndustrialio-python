from ndustrialio.apiservices.tests.unit_tests.test_api_client import TestAPIClient
from ndustrialio.apiservices.tests.integration_tests.test_feeds import TestFeeds
from ndustrialio.workertools.test_runner import TestRunner

if __name__ == '__main__':
    test_runner = TestRunner()
    test_runner.runTests(test_cases=[TestAPIClient, TestFeeds])