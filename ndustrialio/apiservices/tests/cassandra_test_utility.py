from cassandra.cluster import Cluster
import os

class CassandraTestUtility:

    def __init__(self, keyspace, replication="{'class': 'SimpleStrategy', 'replication_factor': '2'}"):
        self.cassandra_cluster = Cluster(contact_points=os.environ.get('CASSANDRA_HOSTS').split(','))
        self.cassandra_con = self.cassandra_cluster.connect()
        self.cassandra_con.execute("CREATE KEYSPACE {} WITH replication = {}".format(keyspace, replication))
        self.cassandra_con.set_keyspace(keyspace)

    def initializeTestData(self, setup_file):
        # Can also batch initialization data using cassandra.query.BatchStatement (only UPDATE, INSERT, DELETE)
        try:
            query_list = self.fileRead(setup_file)
            for query in query_list:
                self.cassandra_con.execute(query)
        except Exception as e:
            print 'Error: Could not insert test data'
            raise e

    def executeQuery(self, query):
        rows = self.cassandra_con.execute(query)
        return rows or []

    def fileRead(self, path):
        dir = os.path.dirname(__file__)
        file_path = os.path.join(dir, path)
        with open(file_path, 'r') as f:
            return f.read().splitlines()

    def close_connection(self):
        print 'Shutting down cassandra cluster...'
        self.cassandra_cluster.shutdown()
