from ndustrialio.apiservices.tests.integration_tests.test_feeds import TestFeeds
from ndustrialio.apiservices.tests.integration_tests.test_rates import TestRates
from ndustrialio.apiservices.tests.unit_tests.test_api_client import TestAPIClient
from ndustrialio.workertools.tests.unit_tests.test_cassandra_utility import TestCassandraUtility
from ndustrialio.testtools.test_runner import TestRunner

if __name__ == '__main__':
    test_runner = TestRunner()
    test_runner.runTests(test_cases=[TestAPIClient,
                                     TestFeeds,
                                     TestRates,
                                     TestCassandraUtility])
