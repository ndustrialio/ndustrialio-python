import unittest
import os
import psycopg2
from ndustrialio.apiservices.feeds import FeedsService

class TestFeeds(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestFeeds, self).__init__(*args, **kwargs)
        self.client_id = os.environ.get('CLIENT_ID')
        self.client_secret = os.environ.get('CLIENT_SECRET')
        self.feeds_service = FeedsService(self.client_id, self.client_secret)
        self.db_con = self.initializeTestDatabase()

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

    def test_get_feed(self):
        self.initializeTestData('./fixtures/setup_get_feeds.sql')
        feed = self.feeds_service.getFeeds(id=4)
        self.assertEqual(feed, 'test')

    def test_get_feeds(self):
        self.initializeTestData('./fixtures/setup_get_feeds.sql')
        feeds = self.feeds_service.getFeeds()
        self.assertEqual(len(feeds), 7)

    def test_get_feed_by_key(self):
        self.initializeTestData('./fixtures/setup_get_feeds.sql')
        feed = self.feeds_service.getFeedByKey(key='key_3')
        self.assertEqual(feed, 'test')

    def test_create_feed(self):
        self.initializeTestData('./fixtures/setup_create_feed.sql')
        response = self.feeds_service.createFeed(key='test_key',
                                                 timezone='UTC',
                                                 type='test_type',
                                                 facility_id=100)
        feed = self.executeQuery('SELECT * from feeds')
        self.assertEqual(feed, 'test')
