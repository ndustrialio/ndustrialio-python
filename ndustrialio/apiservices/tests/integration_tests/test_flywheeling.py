import os
import unittest
from mock import patch
from ndustrialio.apiservices.flywheeling import FlywheelingService
from ndustrialio.workertools.postgres_utility import PostgresUtility

class TestFlywheeling(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.postgres_utility = PostgresUtility(database=os.environ.get('FLYWHEELING_POSTGRES_DB'),
                                               username=os.environ.get('POSTGRES_USER'),
                                               password=os.environ.get('POSTGRES_PASSWORD'),
                                               host=os.environ.get('POSTGRES_HOST'))
        cls.client_id = os.environ.get('FLYWHEELING_CLIENT_ID')
        cls.client_secret = os.environ.get('FLYWHEELING_CLIENT_SECRET')
        cls.api_service_host = os.environ.get('FLYWHEELING_API_SERVICE_HOST')
        cls.audience = os.environ.get('FLYWHEELING_AUDIENCE')
        dir = os.path.dirname(__file__)
        postgres_setup_file_path = os.path.join(dir, 'fixtures/postgres/setup_flywheeling.sql')
        cls.postgres_utility.initDataFromFile(postgres_setup_file_path)
        cls.test_zone_id = cls.postgres_utility.execute('SELECT id FROM zones WHERE name={}'.format('test_zone_name_1'))
        cls.postgres_utility.execute('INSERT INTO runs(zone_id, solver_type, has_solution, name, ran_at) VALUES ({}, {}, {}, {}, {})'.format(cls.test_zone_id,
                                                                                                                                             'convex',
                                                                                                                                             'TRUE',
                                                                                                                                             'test_run_name_1',
                                                                                                                                             '2012-02-08T12:00:00.000Z'))

    # FlywheelingService.getFacilities should return all facilities
    @patch.object(FlywheelingService, 'baseURL')
    @patch.object(FlywheelingService, 'audience')
    def test_get_facilities(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        flywheeling_service = FlywheelingService(client_id=self.client_id, client_secret=self.client_secret)
        facilities = flywheeling_service.getFacilities()
        self.assertEqual(facilities, 'test')

    # FlywheelingService.getSystem should return the specified system
    @patch.object(FlywheelingService, 'baseURL')
    @patch.object(FlywheelingService, 'audience')
    def test_get_system(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        flywheeling_service = FlywheelingService(client_id=self.client_id, client_secret=self.client_secret)
        system = flywheeling_service.getSystem(system_id=2)
        self.assertEqual(system, 'test')

    # FlywheelingService.getSystemsForFacility should return the systems of the specified facility
    @patch.object(FlywheelingService, 'baseURL')
    @patch.object(FlywheelingService, 'audience')
    def test_get_system_for_facility(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        flywheeling_service = FlywheelingService(client_id=self.client_id, client_secret=self.client_secret)
        systems = flywheeling_service.getSystemsForFacility(facility_id=3)
        self.assertEqual(systems, 'test')

    # FlywheelingService.getZonesForSystem should return the zones of the specified system
    @patch.object(FlywheelingService, 'baseURL')
    @patch.object(FlywheelingService, 'audience')
    def test_get_zones_for_system(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        flywheeling_service = FlywheelingService(client_id=self.client_id, client_secret=self.client_secret)
        zones = flywheeling_service.getZonesForSystem(system_id=4)
        self.assertEqual(zones, 'test')

    # FlywheelingService.createRun should create a run with specified parameters
    @patch.object(FlywheelingService, 'baseURL')
    @patch.object(FlywheelingService, 'audience')
    def test_create_run(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        flywheeling_service = FlywheelingService(client_id=self.client_id, client_secret=self.client_secret)
        run = {'zone_id': self.test_zone_id,
               'solver_type': 'convex',
               'has_solution': True,
               'name': 'test_create_run_name',
               'ran_at': '2012-02-08T12:00:00.000Z'}
        flywheeling_service.createRun(run_obj=run)
        try:
            run = self.postgres_utility.execute('SELECT name FROM runs WHERE name={}'.format('test_create_run_name'))
            self.assertEqual(run, 'test')
        finally:
            self.postgres_utility.execute_update('DELETE FROM runs WHERE name={}'.format('test_create_run_name'))

    # FlywheelingService.addDataToRun should add specified data to specified run
    @patch.object(FlywheelingService, 'baseURL')
    @patch.object(FlywheelingService, 'audience')
    def test_add_data_to_run(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        flywheeling_service = FlywheelingService(client_id=self.client_id, client_secret=self.client_secret)
        run_data = {'time': '2012-02-08T12:00:00.000Z',
                    'indicator': True}
        flywheeling_service.addDataToRun(1, run_data)
        try:
            run_data = self.postgres_utility.execute('SELECT * FROM run_data WHERE run_id={} AND time={}'.format(1, '2012-02-08T12:00:00.000Z'))
            self.assertEqual(run_data, 'test')
        finally:
            self.postgres_utility.execute_update('DELETE FROM run_data WHERE run_id={} AND time={}'.format(1, '2012-02-08T12:00:00.000Z'))

    # FlywheelingService.getFacilityAreas should return areas of specified facility (endpoint does not exist)

    # FlywheelingService.addSensorToArea should add specified sensor to specified area (endpoint does not exist)

    # FlywheelingService.getSensorsForArea should return all sensors of specified area (endpoint does not exist)

    # FlyhweelingService.createRunForZone should create run with specified parameters for specified zone (endpoint does not exist)
    @unittest.skip('Endpoint does not exist')
    @patch.object(FlywheelingService, 'baseURL')
    @patch.object(FlywheelingService, 'audience')
    def test_create_run_for_zone(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        flywheeling_service = FlywheelingService(client_id=self.client_id, client_secret=self.client_secret)
        run = {'zone_id': self.test_zone_id,
               'solver_type': 'ncheapest',
               'has_solution': True,
               'name': 'test_create_run_for_zone_name',
               'ran_at': '2012-02-08T12:00:00.000Z'}
        flywheeling_service.createRunForZone(zone_id=self.test_zone_id,
                                             run_obj=run)
        try:
            run = self.postgres_utility.execute('SELECT * FROM run WHERE name={}'.format('test_create_run_for_zone_name'))
            self.assertEqual(run, 'test')
        finally:
            self.postgres_utility.execute_update('DELETE FROM run WHERE name={}'.format('test_create_run_for_zone_name'))

    # FlywheelingService.addDataToZoneRun should add data to the specified run (endpoint does not exist)

    # FlywheelingService.getSystemSetpointData should get setpoint data for specified system (endpoint does not exist)

    # FlywheelingService.getRunsForZones should return runs for specified zone
    @patch.object(FlywheelingService, 'baseURL')
    @patch.object(FlywheelingService, 'audience')
    def test_get_runs_for_zones(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        flywheeling_service = FlywheelingService(client_id=self.client_id, client_secret=self.client_secret)
        runs = flywheeling_service.getRunsForZone(zone_id=self.test_zone_id)
        self.assertEqual(runs, 'test')

    # FlywheelingService.getLatestRunForZone should return latest run for specified zone
    @patch.object(FlywheelingService, 'baseURL')
    @patch.object(FlywheelingService, 'audience')
    def test_get_latest_run_for_zone(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        flywheeling_service = FlywheelingService(client_id=self.client_id, client_secret=self.client_secret)
        latest_run = flywheeling_service.getLatestRunForZone(zone_id=self.test_zone_id)
        self.assertEqual(latest_run, 'test')

    # FlywheelingService.getOutputDataForRun should return output data for specified run (endpoint does not exist)

    # FlywheelingService.addOutputForRun should add output to specified run (endpoint does not exist)

    # FlywheelingService.removeOutputForRun should remove the output of the specified run (endpoint does not exist)

    @classmethod
    def setUpClass(cls):
        cls.postgres_utility.close_connection()