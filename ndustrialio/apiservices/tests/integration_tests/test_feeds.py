import unittest
import os
import psycopg2
from mock import patch
from ndustrialio.apiservices.feeds import FeedsService
from ndustrialio.apiservices.tests import postgres_test_utility as postgres

class TestFeeds(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db_con = psycopg2.connect(database=os.environ.get('POSTGRES_DB'),
                                  user=os.environ.get('POSTGRES_USER'),
                                  password=os.environ.get('POSTGRES_PASSWORD'),
                                  host=os.environ.get('POSTGRES_HOST'))
        db_con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cls.db_con = db_con
        cls.client_id = os.environ.get('CLIENT_ID')
        cls.client_secret = os.environ.get('CLIENT_SECRET')
        cls.api_service_host = os.environ.get('REALTIME_API_SERVICE_HOST')
        cls.audience = os.environ.get('AUDIENCE')
        postgres.initializeTestData(cls.db_con, 'integration_tests/fixtures/setup_feeds.sql')

    # FeedsService.getFeeds should return particular feed if feed id is specified
    @patch.object(FeedsService, 'baseURL')
    @patch.object(FeedsService, 'audience')
    def test_get_feed(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        feeds_service = FeedsService(self.client_id, self.client_secret)
        feed = feeds_service.getFeeds(id=4)
        self.assertEqual(feed['id'], 4)

    # FeedsService.getFeeds should return all feeds if no feed id is specified
    @patch.object(FeedsService, 'baseURL')
    @patch.object(FeedsService, 'audience')
    def test_get_feeds(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        feeds_service = FeedsService(self.client_id, self.client_secret)
        feeds = feeds_service.getFeeds()
        self.assertEqual(len(feeds['records']), 7)

    # FeedsService.getFeedByKey should return all feeds with specified feed key as Paged Response object
    @patch.object(FeedsService, 'baseURL')
    @patch.object(FeedsService, 'audience')
    def test_get_feed_by_key(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        feeds_service = FeedsService(self.client_id, self.client_secret)
        feed = feeds_service.getFeedByKey(key='key_3')
        self.assertEqual(type(feed).__name__, 'PagedResponse')
        self.assertEqual(feed.first()['key'], 'key_3')

    # FeedsService.createFeed should create a feed with the specified attributes
    @patch.object(FeedsService, 'baseURL')
    @patch.object(FeedsService, 'audience')
    def test_create_feed(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        feeds_service = FeedsService(self.client_id, self.client_secret)
        feeds_service.createFeed(key='create_feed_test_key',
                                 timezone='UTC',
                                 type='test_feed_type',
                                 facility_id=100)
        try:
            feed = postgres.executeQuery(self.db_con, "SELECT * FROM feeds WHERE key='create_feed_test_key'")
            self.assertEqual(len(feed), 1)
        finally:
            postgres.executeQuery(self.db_con, "DELETE FROM feeds WHERE key='create_feed_test_key'")

    # FeedsService.createOutput should create an output with the specified attributes
    @patch.object(FeedsService, 'baseURL')
    @patch.object(FeedsService, 'audience')
    def test_create_output(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        feeds_service = FeedsService(self.client_id, self.client_secret)
        feeds_service.createOutput(feed_id=1,
                                   facility_id=20,
                                   label='create_output_test_label',
                                   type='test_output_type')
        try:
            output = postgres.executeQuery(self.db_con, "SELECT * FROM outputs WHERE label='create_output_test_label'")
            self.assertEqual(len(output), 1)
        finally:
            postgres.executeQuery(self.db_con, "DELETE FROM outputs WHERE label='create_output_test_label'")

    # FeedsService.createField should create a field with the specified attributes
    @patch.object(FeedsService, 'baseURL')
    @patch.object(FeedsService, 'audience')
    def test_create_field(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        feeds_service = FeedsService(self.client_id, self.client_secret)
        feeds_service.createField(feed_key='key_1',
                                  output_id=1,
                                  human_name='create_field_test_name',
                                  field_descriptor='test_descriptor')
        try:
            field = postgres.executeQuery(self.db_con, "SELECT * FROM output_fields WHERE human_name='create_field_test_name'")
            self.assertEqual(len(field), 1)
        finally:
            postgres.executeQuery(self.db_con, "DELETE FROM output_fields WHERE human_name='create_field_test_name'")

    # FeedsService.getFieldDescriptors should return fields of specified feed
    @patch.object(FeedsService, 'baseURL')
    @patch.object(FeedsService, 'audience')
    def test_get_field_descriptors(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        feeds_service = FeedsService(self.client_id, self.client_secret)
        field_descriptors = feeds_service.getFieldDescriptors(feed_id=1)
        self.assertEqual(len(field_descriptors['records']), 3)
        self.assertEqual(field_descriptors['_meta']['offset'], 0)

    # FeedsService.getFieldDescriptors with limit smaller than total should return specified number of fields of specified feed
    @patch.object(FeedsService, 'baseURL')
    @patch.object(FeedsService, 'audience')
    def test_get_field_descriptors_limit(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        feeds_service = FeedsService(self.client_id, self.client_secret)
        field_descriptors = feeds_service.getFieldDescriptors(feed_id=1, limit=2)
        self.assertEqual(len(field_descriptors['records']), 2)
        self.assertEqual(field_descriptors['_meta']['offset'], 0)

    # FeedsService.getFieldDescriptors with offset specified should return fields of specified feed based on offset
    @patch.object(FeedsService, 'baseURL')
    @patch.object(FeedsService, 'audience')
    def test_get_field_descriptors_offset(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        feeds_service = FeedsService(self.client_id, self.client_secret)
        field_descriptors = feeds_service.getFieldDescriptors(feed_id=1, offset=2)
        self.assertEqual(len(field_descriptors['records']), 1)
        self.assertEqual(field_descriptors['_meta']['offset'], 2)

    # FeedsService.getUnprovisionedFieldDescriptors should return unprovisioned fields of specified feed

    # FeedsService.getFeedOutputs should return outputs of specified feed
    @patch.object(FeedsService, 'baseURL')
    @patch.object(FeedsService, 'audience')
    def test_get_feed_outputs(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        feeds_service = FeedsService(self.client_id, self.client_secret)
        outputs = feeds_service.getFeedOutputs(feed_id=1)
        self.assertEqual(len(outputs['records']), 2)
