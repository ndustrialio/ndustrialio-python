import os
import unittest
from mock import patch
from ndustrialio.apiservices.weather import WeatherService
from ndustrialio.workertools.postgres_utility import PostgresUtility

class TestWeather(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.postgres_utility = PostgresUtility(database=os.environ.get('WEATHER_POSTGRES_DB'),
                                               username=os.environ.get('POSTGRES_USER'),
                                               password=os.environ.get('POSTGRES_PASSWORD'),
                                               host=os.environ.get('POSTGRES_HOST'))
        cls.client_id = os.environ.get('WEATHER_CLIENT_ID')
        cls.client_secret = os.environ.get('WEATHER_CLIENT_SECRET')
        cls.api_service_host = os.environ.get('WEATHER_API_SERVICE_HOST')
        cls.audience = os.environ.get('WEATHER_AUDIENCE')
        dir = os.path.dirname(__file__)
        postgres_setup_file_path = os.path.join(dir, 'fixtures/postgres/setup_weather.sql')
        cls.postgres_utility.initDataFromFile(postgres_setup_file_path)

    # WeatherService.getForecast should return daily forecast at specified location
    @patch.object(WeatherService, 'baseURL')
    @patch.object(WeatherService, 'audience')
    def test_get_forecast(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        rates_service = WeatherService(self.client_id, self.client_secret)
        forecast = rates_service.getForecast(location_id=1)
        self.assertEqual(forecast, 'true')

    @classmethod
    def tearDownClass(cls):
        cls.postgres_utility.close_connection()