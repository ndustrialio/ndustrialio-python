import os
import unittest
from requests.exceptions import HTTPError
from datetime import datetime
from mock import patch
from ndustrialio.workertools.postgres_utility import PostgresUtility
from ndustrialio.apiservices.rates import RatesService


class TestRates(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.postgres_utility = PostgresUtility(database=os.environ.get('RATES_POSTGRES_DB'),
                                               username=os.environ.get('POSTGRES_USER'),
                                               password=os.environ.get('POSTGRES_PASSWORD'),
                                               host=os.environ.get('POSTGRES_HOST'))
        cls.client_id = os.environ.get('RATES_CLIENT_ID')
        cls.client_secret = os.environ.get('RATES_CLIENT_SECRET')
        cls.api_service_host = os.environ.get('RATES_API_SERVICE_HOST')
        cls.audience = os.environ.get('RATES_AUDIENCE')
        dir = os.path.dirname(__file__)
        postgres_setup_file_path = os.path.join(dir, 'fixtures/postgres/setup_rates.sql')
        cls.postgres_utility.initDataFromFile(postgres_setup_file_path)

    # RatesService.getSchedules should return all schedules
    @patch.object(RatesService, 'baseURL')
    @patch.object(RatesService, 'audience')
    def test_get_schedules(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        rates_service = RatesService(self.client_id, self.client_secret)
        schedules = rates_service.getSchedules()
        self.assertEqual(len(schedules['records']), 5)

    # RatesService.getScheduleInfo should return information of specified rate schedule
    @patch.object(RatesService, 'baseURL')
    @patch.object(RatesService, 'audience')
    def test_get_schedule_info(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        rates_service = RatesService(self.client_id, self.client_secret)
        schedule_info = rates_service.getScheduleInfo(rate_schedule_id=2)
        self.assertEqual(schedule_info['label'], 'test_schedule_label_2')

    # RatesService.getScheduleRTPPeriods should return RTP periods of specified rate schedule
    @patch.object(RatesService, 'baseURL')
    @patch.object(RatesService, 'audience')
    def test_get_schedule_rtp_periods(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        rates_service = RatesService(self.client_id, self.client_secret)
        rtp_periods = rates_service.getScheduleRTPPeriods(id=1)
        self.assertEqual(len(rtp_periods['records']), 2)

    # RatesServie.getScheduleRTPPeriods with orderBy specified should return RTP periods of specified rate schedule in the appropriate order
    @patch.object(RatesService, 'baseURL')
    @patch.object(RatesService, 'audience')
    def test_get_schedule_rtp_periods_order_by(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        rates_service = RatesService(self.client_id, self.client_secret)
        rtp_periods = rates_service.getScheduleRTPPeriods(id=1, orderBy='period_end')
        first_end_time = datetime.strptime(str(rtp_periods['records'][0]['period_end']), '%Y-%m-%dT%H:%M:%S.%fZ')
        second_end_time = datetime.strptime(str(rtp_periods['records'][1]['period_end']), '%Y-%m-%dT%H:%M:%S.%fZ')
        self.assertTrue(second_end_time > first_end_time)

    # RatesService.getScheduleRTPPeriods with orderBy specified and reverseOrder=True should return RTP periods of specified rate schedule in the appropriate reverse order
    @patch.object(RatesService, 'baseURL')
    @patch.object(RatesService, 'audience')
    def test_get_schedule_rtp_periods_reverse_order_end(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        rates_service = RatesService(self.client_id, self.client_secret)
        rtp_periods = rates_service.getScheduleRTPPeriods(id=1, orderBy='period_end', reverseOrder=True)
        first_end_time = datetime.strptime(str(rtp_periods['records'][0]['period_end']), '%Y-%m-%dT%H:%M:%S.%fZ')
        second_end_time = datetime.strptime(str(rtp_periods['records'][1]['period_end']), '%Y-%m-%dT%H:%M:%S.%fZ')
        self.assertTrue(first_end_time > second_end_time)

    # RatesService.getScheduleRTPPeriods with orderBy not specified and reverseOrder=True should return RTP periods of specified rate schedule in the appropriate reverse order
    @patch.object(RatesService, 'baseURL')
    @patch.object(RatesService, 'audience')
    def test_get_schedule_rtp_periods_reverse_order_start(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        rates_service = RatesService(self.client_id, self.client_secret)
        rtp_periods = rates_service.getScheduleRTPPeriods(id=1, reverseOrder=True)
        first_start_time = datetime.strptime(str(rtp_periods['records'][0]['period_start']), '%Y-%m-%dT%H:%M:%S.%fZ')
        second_start_time = datetime.strptime(str(rtp_periods['records'][1]['period_start']), '%Y-%m-%dT%H:%M:%S.%fZ')
        self.assertTrue(first_start_time > second_start_time)

    # RatesService.getScheduleRTPPeriods should return error if rate schedule is non-rtp
    @patch.object(RatesService, 'baseURL')
    @patch.object(RatesService, 'audience')
    def test_get_schedule_rtp_periods_non_rtp(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        rates_service = RatesService(self.client_id, self.client_secret)
        self.assertRaises(HTTPError, rates_service.getScheduleRTPPeriods, 3)

    # RatesService.getUsagePeriods should return usage periods of specified rate schedule in the specified time range
    @unittest.skip('Raises error: Bad Request - No valid seasons for this season type')
    @patch.object(RatesService, 'baseURL')
    @patch.object(RatesService, 'audience')
    def test_get_usage_periods(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        rates_service = RatesService(self.client_id, self.client_secret)
        usage_periods = rates_service.getUsagePeriods(id=3,
                                                      timeStart=datetime.strptime('2012-02-08T12:00:00.000Z',
                                                                                  '%Y-%m-%dT%H:%M:%S.%fZ'),
                                                      timeEnd=datetime.strptime('2012-03-08T12:00:00.000Z',
                                                                                '%Y-%m-%dT%H:%M:%S.%fZ'))
        self.assertEqual(usage_periods, 'test')

    # RatesService.getDemandPeriods with season_type specified should return demand periods of specified rate schedule in the specified time range corresponding to the specified season_type
    @unittest.skip('Raises error: Bad Request - No valid seasons for this season type')
    @patch.object(RatesService, 'baseURL')
    @patch.object(RatesService, 'audience')
    def test_get_demand_periods(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        rates_service = RatesService(self.client_id, self.client_secret)
        demand_periods = rates_service.getDemandPeriods(id=3,
                                                        timeStart=datetime.strptime('2012-02-08T12:00:00.000Z',
                                                                                    '%Y-%m-%dT%H:%M:%S.%fZ'),
                                                        timeEnd=datetime.strptime('2012-03-08T12:00:00.000Z',
                                                                                  '%Y-%m-%dT%H:%M:%S.%fZ'),
                                                        season_type='tou')
        self.assertEqual(demand_periods, 'test')

    # RatesService.getRTPPeriod should return specified rtp period
    @patch.object(RatesService, 'baseURL')
    @patch.object(RatesService, 'audience')
    def test_get_rtp_periods(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        rates_service = RatesService(self.client_id, self.client_secret)
        rtp_period = rates_service.getRTPPeriod(id=3)
        self.assertEqual(rtp_period['title'], 'test_period_title_3')

    @classmethod
    def tearDownClass(cls):
        cls.postgres_utility.close_connection()