import os
import psycopg2
from ndustrialio.workertools.postgres_utility import PostgresUtility

class PostgresTestUtility(PostgresUtility):

    def __init__(self, database, user, password, host):
        self.connection = psycopg2.connect(dbname=database,
                                           host=host,
                                           user=user,
                                           password=password)
        self.connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    def initTestDataFromFile(self, setup_file=None):
        try:
            with self.connection.cursor() as cur:
                cur.execute(self.fileRead(setup_file))
        except Exception as e:
            print 'Error: Could not insert test data'
            raise e

    def executeQuery(self, query):
        rows = []
        with self.connection.cursor() as cur:
            cur.execute(query)
            try:
                rows = cur.fetchall()
            except Exception:
                pass
        return rows

    def fileRead(self, path):
        dir = os.path.dirname(__file__)
        file_path = os.path.join(dir, path)
        with open(file_path, 'r') as f:
            return f.read()

    def close_connection(self):
        print 'Closing postgres connection...'
        self.connection.close()