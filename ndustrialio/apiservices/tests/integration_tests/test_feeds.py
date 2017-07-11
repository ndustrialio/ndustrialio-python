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
                cur.execute('DROP DATABASE IF EXISTS {}'.format(os.environ.get('POSTGRES_DB')))
                cur.execute('CREATE DATABASE {}'.format(os.environ.get('POSTGRES_DB')))
                cur.execute(self.fileRead(psql_setup_file))

    def fileRead(self, path):
        dir = os.path.dirname(__file__)
        file_path = os.path.join(dir, path)
        with open(file_path, 'r') as f:
            return f.read()

    def test_get_feeds(self):
        self.initializeTestData('./fixtures/setup_get_feeds.sql')