import os
import unittest
from datetime import datetime
from freezegun import freeze_time
from ndustrialio.workertools.cassandra_utility import CassandraUtility

class TestCassandraUtility(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cassandra_utility = CassandraUtility(host=os.environ.get('CASSANDRA_HOSTS').split(',')[0],
                                                 keyspace=os.environ.get('CASSANDRA_KEYSPACE'),
                                                 consistency_level=None)
        dir = os.path.dirname(__file__)
        cassandra_setup_file_path = os.path.join(dir, 'fixtures/cassandra/setup_cassandra_utility.cql')
        cls.cassandra_utility.initDataFromFile(cassandra_setup_file_path)

    # CassandraUtility.getActiveOutputs should return all active outputs
    @freeze_time('2015-01-19T12:00:00.000Z')
    def test_get_active_outputs(self):
        outputs = self.cassandra_utility.getActiveOutputs()
        self.assertEqual(outputs, {1: [u'test_field_2', u'test_field_1', u'test_field_2'],
                                   2: [u'test_field_3'],
                                   3: [u'test_field_3', u'test_field_4']})

    # CassandraUtility.getActiveOutputs with output_filter specified should return all active outputs that match specified filter
    @freeze_time('2015-01-19T12:00:00.000Z')
    def test_get_active_outputs_output_filter(self):
        outputs = self.cassandra_utility.getActiveOutputs(output_filter=[1, 3])
        self.assertEqual(outputs, {1: [u'test_field_2', u'test_field_1', u'test_field_2'],
                                   3: [u'test_field_3', u'test_field_4']})

    # CassandraUtility.getActiveOutputs with field_filter specified should return all active outputs with fields that match specified filter
    @freeze_time('2015-01-19T12:00:00.000Z')
    def test_get_active_outputs_field_filter(self):
        outputs = self.cassandra_utility.getActiveOutputs(field_filter=['test_field_2', 'test_field_4'])
        self.assertEqual(outputs, {1: [u'test_field_2', u'test_field_2'],
                                   3: [u'test_field_4']})

    # CassandraUtility.getActiveOutputs with output_filter and field_filter specified should return all active outputs with fields that match specified filters
    @freeze_time('2015-01-19T12:00:00.000Z')
    def test_get_active_outputs_both_filters(self):
        outputs = self.cassandra_utility.getActiveOutputs(output_filter=[1,3],
                                                          field_filter=['test_field_1', 'test_field_4'])
        self.assertEqual(outputs, {1: [u'test_field_1'],
                                   3: [u'test_field_4']})

    # CassandraUtility.getData with time_end not specified should return timeseries data for specified field after time_start
    @unittest.skip('Raises error: No indexed columns present in by-columns clause with Equal operator')
    def test_get_data(self):
        data = self.cassandra_utility.getData(output_id=2,
                                              field_human_name='test_field_2',
                                              time_start=datetime.strptime('2015-02-20T01:00:00.000Z',
                                                                           '%Y-%m-%dT%H:%M:%S.%fZ'),
                                              window=1)
        self.assertEqual(data, 'test')

    # CassandraUtility.getData with time_end specified should return timeseries data for specified field in specified time range
    @unittest.skip('Raises error: No indexed columns present in by-columns clause with Equal operator')
    def test_get_data_time_range(self):
        data = self.cassandra_utility.getData(output_id=2,
                                              field_human_name='test_field_2',
                                              time_start=datetime.strptime('2015-02-20T01:00:00.000Z',
                                                                           '%Y-%m-%dT%H:%M:%S.%fZ'),
                                              window=1,
                                              time_end=datetime.strptime('2015-03-30T01:00:00.000Z',
                                                                           '%Y-%m-%dT%H:%M:%S.%fZ'))
        self.assertEqual(data, 'test')

    @classmethod
    def tearDownClass(cls):
        cls.cassandra_utility.drop_keyspace(os.environ.get('CASSANDRA_KEYSPACE'))
        cls.cassandra_utility.close_connection()
