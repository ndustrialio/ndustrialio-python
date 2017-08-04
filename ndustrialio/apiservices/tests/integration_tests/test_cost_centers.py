import os
import unittest
from mock import patch
from ndustrialio.apiservices.costcenters import CostCentersService
from ndustrialio.workertools.postgres_utility import PostgresUtility

class TestCostCenters(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.postgres_utility = PostgresUtility(database=os.environ.get('COST_CENTERS_POSTGRES_DB'),
                                               username=os.environ.get('POSTGRES_USER'),
                                               password=os.environ.get('POSTGRES_PASSWORD'),
                                               host=os.environ.get('POSTGRES_HOST'))
        cls.client_id = os.environ.get('COST_CENTERS_CLIENT_ID')
        cls.client_secret = os.environ.get('COST_CENTERS_CLIENT_SECRET')
        cls.api_service_host = os.environ.get('COST_CENTERS_API_SERVICE_HOST')
        cls.audience = os.environ.get('COST_CENTERS_AUDIENCE')
        dir = os.path.dirname(__file__)
        postgres_setup_file_path = os.path.join(dir, 'fixtures/postgres/setup_cost_centers.sql')
        cls.postgres_utility.initDataFromFile(postgres_setup_file_path)
        cls.test_cost_center_id = cls.postgres_utility.execute('SELECT id FROM cost_centers WHERE name={}'.format('test_cost_center_name_1'))['id']
        cls.test_attribute_id = cls.postgres_utility.execute('SELECT id FROM attributes WHERE name={}'.format('test_attribute_name_1'))['id']
        cls.postgres_utility.execute('INSERT INTO cost_center_attributes(attribute_id, cost_center_id, track_budget, track_forecast, track_actuals) VALUES ({}, {}, {}, {}, {}'.format(cls.test_attribute_id,
                                                                                                                                                                                       cls.test_cost_center_id,
                                                                                                                                                                                       'TRUE',
                                                                                                                                                                                       'FALSE',
                                                                                                                                                                                       'TRUE'))
        cls.test_cost_center_attribute_id = cls.postgres_utility.execute('SELECT id FROM cost_center_attributes WHERE track_forecast={}'.format('FALSE'))['id']

    # CostCentersService.addCostCenter should create cost center with the specified attributes
    @patch.object(CostCentersService, 'baseURL')
    @patch.object(CostCentersService, 'audience')
    def test_add_cost_center(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        cost_centers_service = CostCentersService(self.client_id, self.client_secret)
        cost_center = {'name': 'test_cost_center_name',
                       'descriptor': 'test_cost_center_descriptor',
                       'facility_id': 1,
                       'activity_start': '2000-16-08 04:05:06'}
        cost_centers_service.addCostCenter(cost_center_obj=cost_center)
        try:
            cost_center = self.postgres_utility.execute('SELECT * FROM cost_centers WHERE name={}'.format('test_cost_center_name'))
            self.assertEqual(cost_center, 'test')
        finally:
            self.postgres_utility.execute_update('DELETE FROM cost_centers WHERE name={}'.format('test_cost_center_name'))

    # CostCentersService.addAttribute should create the specified attribute
    @patch.object(CostCentersService, 'baseURL')
    @patch.object(CostCentersService, 'audience')
    def test_add_attribute(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        cost_centers_service = CostCentersService(self.client_id, self.client_secret)
        attribute = {'is_default': True,
                     'name': 'test_attribute_name',
                     'type': 'test_attribute_type',
                     'units': 'test_attribute_unit',
                     }
        cost_centers_service.addAttribute(attribute_obj=attribute)
        try:
            attribute = self.postgres_utility.execute('SELECT * FROM attributes WHERE name={}'.format('test_attribute_name'))
            self.assertEqual(attribute, 'test')
        finally:
            self.postgres_utility.execute_update('DELETE FROM attributes WHERE name={}'.format('test_attribute_name'))

    # CostCentersService.getCostCenterAttributes should return all attributes of the specified cost center
    @patch.object(CostCentersService, 'baseURL')
    @patch.object(CostCentersService, 'audience')
    def test_get_cost_center_attributes(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        cost_centers_service = CostCentersService(self.client_id, self.client_secret)
        attributes = cost_centers_service.getCostCenterAttributes(cost_center_id=self.test_cost_center_id)
        self.assertEqual(attributes, 'test')

    # CostCentersService.addCostCenterAttribute should create cost center attribute with specified cost center and attribute id's
    @patch.object(CostCentersService, 'baseURL')
    @patch.object(CostCentersService, 'audience')
    def test_add_cost_center_attribute(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        cost_centers_service = CostCentersService(self.client_id, self.client_secret)
        cost_centers_service.addCostCenterAttribute(cost_center_id=self.test_cost_center_id,
                                                    attribute_id=self.test_attribute_id,
                                                    track_budget=False,
                                                    track_forecast=True,
                                                    track_actuals=False)
        try:
            attribute = self.postgres_utility.execute('SELECT * FROM cost_center_attributes WHERE track_forecast={}'.format('TRUE'))
            self.assertEqual(attribute, 'test')
        finally:
            self.postgres_utility.execute_update('DELETE FROM cost_center_attributes WHERE track_forecast={}'.format('TRUE'))

    # CostCenterService.addCostCenterActual should create cost center actual with specified fields
    @patch.object(CostCentersService, 'baseURL')
    @patch.object(CostCentersService, 'audience')
    def test_add_cost_center_actual(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        cost_centers_service = CostCentersService(self.client_id, self.client_secret)
        actual_obj = {'activity_start': '2000-12-08 04:05:06',
                      'activity_end': '2000-15-08 04:05:06',
                      'value': 5.0}
        cost_centers_service.addCostCenterActual(cost_center_attribute_id=self.test_cost_center_attribute_id,
                                                 actuals_obj=actual_obj)
        try:
            actual = self.postgres_utility.execute('SELECT * FROM cost_center_actuals WHERE value={}'.format(5.0))
            self.assertEqual(actual, 'test')
        finally:
            self.postgres_utility.execute_update('DELETE FROM cost_center_actuals WHERE value={}'.format(5.0))

    # CostCenterService.addCostCenterBudget should create cost center budget with specified fields
    @patch.object(CostCentersService, 'baseURL')
    @patch.object(CostCentersService, 'audience')
    def test_add_cost_center_budget(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        cost_centers_service = CostCentersService(self.client_id, self.client_secret)
        budget_obj = {'activity_start': '2000-12-08 04:05:06',
                      'activity_end': '2000-20-08 04:05:06',
                      'value': 5.0}
        cost_centers_service.addCostCenterBudget(cost_center_attribute_id=self.test_cost_center_attribute_id,
                                                 budget_obj=budget_obj)
        try:
            budget = self.postgres_utility.execute('SELECT * FROM cost_center_budgets WHERE value={}'.format(5.0))
            self.assertEqual(budget, 'test')
        finally:
            self.postgres_utility.execute_update('DELETE FROM cost_center_budgets WHERE value={}'.format(5.0))


    @classmethod
    def tearDownClass(cls):
        cls.postgres_utility.close_connection()