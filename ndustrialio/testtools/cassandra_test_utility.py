import os
from cassandra.cluster import Cluster
from ndustrialio.workertools.cassandra_utility import CassandraUtility

class CassandraTestUtility(CassandraUtility):

    def __init__(self, keyspace, replication="{'class': 'SimpleStrategy', 'replication_factor': '2'}"):
        self.cluster = Cluster(contact_points=os.environ.get('CASSANDRA_HOSTS').split(','))
        self.session = self.cluster.connect()
        self.session.execute("CREATE KEYSPACE {} WITH REPLICATION = {}".format(keyspace, replication))
        self.session.set_keyspace(keyspace)

    def initTestDataFromFile(self, setup_file):
        # Can also batch initialization data using cassandra.query.BatchStatement (only UPDATE, INSERT, DELETE)
        try:
            query_list = self.fileRead(setup_file)
            for query in query_list:
                self.execute(query)
        except Exception as e:
            print 'Error: Could not insert test data'
            raise e

    def fileRead(self, path):
        with open(path, 'r') as f:
            return f.read().splitlines()

    def close_connection(self):
        print 'Shutting down cassandra cluster...'
        self.cluster.shutdown()