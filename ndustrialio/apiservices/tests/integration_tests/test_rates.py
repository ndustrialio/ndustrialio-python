import os
import unittest
from mock import patch
from ndustrialio.workertools.postgres_utility import PostgresUtility
from ndustrialio.apiservices.rates import RatesService


class TestFeeds(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.postgres_utility = PostgresUtility(database=os.environ.get('POSTGRES_DB'),
                                               username=os.environ.get('POSTGRES_USER'),
                                               password=os.environ.get('POSTGRES_PASSWORD'),
                                               host=os.environ.get('POSTGRES_HOST'))
        cls.client_id = os.environ.get('CLIENT_ID')
        cls.client_secret = os.environ.get('CLIENT_SECRET')
        cls.api_service_host = os.environ.get('RATES_API_SERVICE_HOST')
        cls.audience = os.environ.get('RATES_AUDIENCE')
        dir = os.path.dirname(__file__)
        postgres_setup_file_path = os.path.join(dir, 'fixtures/postgres/setup_feeds.sql')
        cls.postgres_utility.initDataFromFile(postgres_setup_file_path)

    # RatesService.getSchedules should return all schedules

    # RatesService.getScheduleInfo should return information of specified rate schedule

    # RatesService.getScheduleRTPPeriods should return RTP periods of specified rate schedule

    # RatesServie.getScheduleRTPPeriods with orderBy specified should return RTP periods of specified rate schedule in the appropriate order

    # RatesService.getScheduleRTPPeriods with orderBy specified and reverseOrder=True should return RTP periods of specified rate schedule in the appropriate reverse order

    # RatesService.getScheduleRTPPeriods with orderBy not specified and reverseOrder=True should raise an error or ignore the reverseOrder arg

    # RatesService.getUsagePeriods should return usage periods of specified rate schedule in the specified time range

    # RatesService.getDemandPeriods should return demand periods of specified rate schedule in the specified time range

    # RatesService.getDemandPeriods with season_type specified should return demand periods of specified rate schedule in the specified time range corresponding to the specified season_type

    # RatesService.getRTPPeriod should return RTP periods of specified rate period

