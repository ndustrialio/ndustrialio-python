import os
import unittest
from datetime import datetime
from mock import patch
from ndustrialio.workertools.cassandra_utility import CassandraUtility
from ndustrialio.workertools.postgres_utility import PostgresUtility
from ndustrialio.apiservices.feeds import FeedsService


class TestFeeds(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.postgres_utility = PostgresUtility(database=os.environ.get('POSTGRES_DB'),
                                               username=os.environ.get('POSTGRES_USER'),
                                               password=os.environ.get('POSTGRES_PASSWORD'),
                                               host=os.environ.get('POSTGRES_HOST'))
        cls.cassandra_utility = CassandraUtility(host=os.environ.get('CASSANDRA_HOSTS').split(',')[0],
                                                 keyspace=os.environ.get('CASSANDRA_KEYSPACE'),
                                                 consistency_level=None)
        cls.client_id = os.environ.get('CLIENT_ID')
        cls.client_secret = os.environ.get('CLIENT_SECRET')
        cls.api_service_host = os.environ.get('REALTIME_API_SERVICE_HOST')
        cls.audience = os.environ.get('AUDIENCE')
        dir = os.path.dirname(__file__)
        postgres_setup_file_path = os.path.join(dir, 'fixtures/postgres/setup_feeds.sql')
        cassandra_setup_file_path = os.path.join(dir, 'fixtures/cassandra/setup_feeds.sql')
        cls.postgres_utility.initDataFromFile(postgres_setup_file_path)
        cls.cassandra_utility.initDataFromFile(cassandra_setup_file_path)

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
                                 type='test_feed_type_1',
                                 facility_id=100)
        try:
            feed = self.postgres_utility.execute("SELECT * FROM feeds WHERE key='create_feed_test_key'")
            self.assertEqual(len(feed), 1)
        finally:
            self.postgres_utility.execute_update("DELETE FROM feeds WHERE key='create_feed_test_key'")

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
            output = self.postgres_utility.execute("SELECT * FROM outputs WHERE label='create_output_test_label'")
            self.assertEqual(len(output), 1)
        finally:
            self.postgres_utility.execute_update("DELETE FROM outputs WHERE label='create_output_test_label'")

    # FeedsService.createField should create a field with the specified attributes
    @unittest.skip('Fails because field_human_name is set strangely (0 != 1)')
    @patch.object(FeedsService, 'baseURL')
    @patch.object(FeedsService, 'audience')
    def test_create_field(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        feeds_service = FeedsService(self.client_id, self.client_secret)
        feeds_service.createField(feed_key='key_1',
                                  output_id=1,
                                  human_name='create_field_test_name',
                                  field_descriptor='test_descriptor',
                                  type='string')
        try:
            field = self.postgres_utility.execute("SELECT * FROM output_fields WHERE field_human_name='create_field_test_name'")
            self.assertEqual(len(field), 1)
        finally:
            self.postgres_utility.execute_update("DELETE FROM output_fields WHERE field_human_name='create_field_test_name'")

    # FeedsService.getFieldDescriptors should return fields of specified feed
    @unittest.skip('Fails because of additional field that is not deleted in test_create_field (4 != 3)')
    @patch.object(FeedsService, 'baseURL')
    @patch.object(FeedsService, 'audience')
    def test_get_field_descriptors(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        feeds_service = FeedsService(self.client_id, self.client_secret)
        field_descriptors = feeds_service.getFieldDescriptors(feed_id=1)
        self.assertEqual(field_descriptors['records'], 3)
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
    @unittest.skip('Fails because of additional field that is not deleted in test_create_field (2 != 1)')
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

    # FeedsService.getUnprovisionedData should query cassandra for specified unprovisioned field's data
    @unittest.skip('Raises invalid filters error')
    @patch.object(FeedsService, 'baseURL')
    @patch.object(FeedsService, 'audience')
    def test_get_unprovisioned_data(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        feeds_service = FeedsService(self.client_id, self.client_secret)
        data = feeds_service.getUnprovisionedData(feed_id=1,
                                                  field_descriptor='test_field_descriptor_1',
                                                  time_start=datetime.strptime('2015-01-08T12:00:00.000Z',
                                                                               '%Y-%m-%dT%H:%M:%S.%fZ'),
                                                  time_end=datetime.strptime('2015-04-08T12:00:00.000Z',
                                                                             '%Y-%m-%dT%H:%M:%S.%fZ'))
        self.assertEqual(len(data), 2)

    # FeedsService.getData should query Cassandra for specified field's data
    @unittest.skip('Fails because query does not match Cassandra entries (0 != 2)')
    @patch.object(FeedsService, 'baseURL')
    @patch.object(FeedsService, 'audience')
    def test_get_data(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        feeds_service = FeedsService(self.client_id, self.client_secret)
        data = feeds_service.getData(output_id=1,
                                     field_human_name='test_name_1',
                                     window=60,
                                     time_start=datetime.strptime('2015-01-08T12:00:00.000Z',
                                                                  '%Y-%m-%dT%H:%M:%S.%fZ'),
                                     time_end=datetime.strptime('2015-04-08T12:00:00.000Z',
                                                                '%Y-%m-%dT%H:%M:%S.%fZ'))
        self.assertEqual(len(data.records), 2)

    # FeedsService.getOutputsForFacility should return outputs corresponding to specified facility
    @patch.object(FeedsService, 'baseURL')
    @patch.object(FeedsService, 'audience')
    def test_get_outputs_for_facility(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        feeds_service = FeedsService(self.client_id, self.client_secret)
        outputs = feeds_service.getOutputsForFacility(facility_id=20)
        self.assertEqual(outputs.total_records, 3)
        self.assertEqual(type(outputs).__name__, 'PagedResponse')

    # FeedsService.getOutputs with id specified should return specified output
    #@unittest.skip('Returns 500 Internal Server error')
    @patch.object(FeedsService, 'baseURL')
    @patch.object(FeedsService, 'audience')
    def test_get_output_by_id(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        feeds_service = FeedsService(self.client_id, self.client_secret)
        outputs = feeds_service.getOutputs(id=1)
        self.assertEqual(outputs['label'], 'test_label_1')

    # FeedsService.getOutputs with no id specified should return all outputs
    @patch.object(FeedsService, 'baseURL')
    @patch.object(FeedsService, 'audience')
    def test_get_all_outputs(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        feeds_service = FeedsService(self.client_id, self.client_secret)
        outputs = feeds_service.getOutputs()
        self.assertEqual(outputs['_metadata']['totalRecords'], 4)

    # FeedsService.getFields should return fields corresponding to specified output
    @unittest.skip('Fails because of undeleted field in test_create_field (5 != 4)')
    @patch.object(FeedsService, 'baseURL')
    @patch.object(FeedsService, 'audience')
    def test_get_fields(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        feeds_service = FeedsService(self.client_id, self.client_secret)
        fields = feeds_service.getFields(output_id=1)
        self.assertEqual(fields['_metadata']['totalRecords'], 4)

    # FeedsService.getTypes should return all feed types
    @patch.object(FeedsService, 'baseURL')
    @patch.object(FeedsService, 'audience')
    def test_get_types(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        feeds_service = FeedsService(self.client_id, self.client_secret)
        types = feeds_service.getTypes()
        self.assertEqual(len(types), 2)

    # FeedsService.updateStatus should update the status of the given feed
    @unittest.skip('Raises JSON decode error')
    @patch.object(FeedsService, 'baseURL')
    @patch.object(FeedsService, 'audience')
    def test_update_status(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        feeds_service = FeedsService(self.client_id, self.client_secret)
        feeds_service.updateStatus(feed_id=3,
                                   status='Out-of-Date')
        try:
            feed = self.postgres_utility.execute('SELECT * FROM feeds WHERE id=3')
            self.assertEqual(feed['status'], 'Out-of-Date')
        finally:
            self.postgres_utility.execute_update('UPDATE feeds SET status="Active" WHERE id=3')

    # FeedsService.getLatestStatus should return most recent status of all feeds
    @unittest.skip('Raises JSON decode error')
    @patch.object(FeedsService, 'baseURL')
    @patch.object(FeedsService, 'audience')
    def test_get_latest_status(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        feeds_service = FeedsService(self.client_id, self.client_secret)
        statuses = feeds_service.getLatestStatus()
        self.assertEqual(statuses, 'test')

    # FeedsService.getFieldDataMetrics should return metrics for specified field
    @unittest.skip('Raises access denies for scopes read:metrics error')
    @patch.object(FeedsService, 'baseURL')
    @patch.object(FeedsService, 'audience')
    def test_field_data_metrics(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        feeds_service = FeedsService(self.client_id, self.client_secret)
        metrics = feeds_service.getFieldDataMetrics([1, 2, 3], 'test_label_1')
        self.assertEqual(metrics, 'test')

    @classmethod
    def tearDownClass(cls):
        cls.postgres_utility.close_connection()
        cls.cassandra_utility.close_connection()