import unittest
import os
import psycopg2
from mock import patch
from ndustrialio.apiservices.feeds import FeedsService

class TestFeeds(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestFeeds, self).__init__(*args, **kwargs)
        self.client_id = os.environ.get('CLIENT_ID')
        self.client_secret = os.environ.get('CLIENT_SECRET')
        self.db_con = self.initializeTestDatabase()
        self.api_service_host = os.environ.get('REALTIME_API_SERVICE_HOST')
        self.audience = os.environ.get('AUDIENCE')

    def initializeTestDatabase(self):
        db_con = psycopg2.connect(database=os.environ.get('POSTGRES_DB'),
                                  user=os.environ.get('POSTGRES_USER'),
                                  password=os.environ.get('POSTGRES_PASSWORD'),
                                  host=os.environ.get('POSTGRES_HOST'))
        db_con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        return db_con

    def initializeTestData(self, psql_setup_file=None):
        if psql_setup_file:
            with self.db_con.cursor() as cur:
                cur.execute(self.fileRead(psql_setup_file))

    def fileRead(self, path):
        dir = os.path.dirname(__file__)
        file_path = os.path.join(dir, path)
        with open(file_path, 'r') as f:
            return f.read()

    def executeQuery(self, query, args=None):
        with self.db_con.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
        return rows

    # FeedsService.getFeeds should return particular feed if feed id is specified
    @patch.object(FeedsService, 'baseURL')
    @patch.object(FeedsService, 'audience')
    def test_get_feed(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        feeds_service = FeedsService(self.client_id, self.client_secret)
        self.initializeTestData('./fixtures/setup_get_feeds.sql')
        feed = feeds_service.getFeeds(id=4)
        self.assertEqual(feed, 'test')

    # FeedsService.getFeeds should return all feeds if no feed id is specified
    @patch.object(FeedsService, 'baseURL')
    @patch.object(FeedsService, 'audience')
    def test_get_feeds(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        feeds_service = FeedsService(self.client_id, self.client_secret)
        self.initializeTestData('./fixtures/setup_get_feeds.sql')
        feeds = feeds_service.getFeeds()
        self.assertEqual(len(feeds), 7)

    # FeedsService.getFeedByKey should return all feeds with specified feed key as Paged Response object
    @patch.object(FeedsService, 'baseURL')
    @patch.object(FeedsService, 'audience')
    def test_get_feed_by_key(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        feeds_service = FeedsService(self.client_id, self.client_secret)
        self.initializeTestData('./fixtures/setup_get_feeds.sql')
        feed = feeds_service.getFeedByKey(key='key_3')
        self.assertEqual(feed, 'test')

    # FeedsService.createFeed should create a feed with the specified attributes
    @patch.object(FeedsService, 'baseURL')
    @patch.object(FeedsService, 'audience')
    def test_create_feed(self, mock_audience, mock_baseURL):
        mock_audience.return_value = self.audience
        mock_baseURL.return_value = 'http://{}:3000'.format(self.api_service_host)
        feeds_service = FeedsService(self.client_id, self.client_secret)
        self.initializeTestData('./fixtures/setup_create_feed.sql')
        response = feeds_service.createFeed(key='test_key',
                                                 timezone='UTC',
                                                 type='test_type',
                                                 facility_id=100)
        feed = self.executeQuery('SELECT * from feeds')
        self.assertEqual(feed, 'test')

    #