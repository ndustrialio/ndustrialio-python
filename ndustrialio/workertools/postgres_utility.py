import psycopg2
import psycopg2.extras

class PostgresUtility:

    def __init__(self, host, username, password, database):

        self.connection = psycopg2.connect(dbname=database,
                                           host=host,
                                           user=username,
                                           password=password)


    def execute(self, statement, args=None):

        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


        if args is not None:

            cursor.execute(statement, args)

        else:

            cursor.execute(statement)

        res = cursor.fetchall()

        cursor.close()

        return res


    def execute_update(self, statement, args=None):

        cursor = self.connection.cursor()

        if args is not None:

            cursor.execute(statement, args)

        else:

            cursor.execute(statement)

        self.connection.commit()
        cursor.close()

    def initDataFromFile(self, setup_file=None):
        try:
            with self.connection.cursor() as cur:
                cur.execute(self.fileRead(setup_file))
        except Exception as e:
            print 'Error: Could not insert test data'
            self.connection.rollback()
            raise e
        self.connection.commit()

    def fileRead(self, path):
        with open(path, 'r') as f:
            return f.read()

    def close_connection(self):
        print 'Closing postgres connection...'
        self.connection.close()
