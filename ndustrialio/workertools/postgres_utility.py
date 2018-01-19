import psycopg2
import psycopg2.extras

class PostgresUtility:

    def __init__(self, host, username, password, database):

        self.connection = psycopg2.connect(dbname=database,
                                           host=host,
                                           user=username,
                                           password=password)

        psycopg2.extras.register_uuid()


    def execute(self, statement, args=None):

        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        try:
            if args is not None:

                cursor.execute(statement, args)

            else:

                cursor.execute(statement)

        except psycopg2.Error as e:
            cursor.close()

            raise e

        res = cursor.fetchall()
        cursor.close()


        return res


    def execute_update(self, statement, args=None, auto_commit=True, returning=False):

        cursor = self.connection.cursor()

        try:

            if args is not None:

                cursor.execute(statement, args)

            else:

                cursor.execute(statement)

        except psycopg2.Error as e:
            cursor.close()
            self.connection.rollback()

            raise e


        if auto_commit:

            self.connection.commit()

        if returning:
            ret = cursor.fetchone()[0]
            cursor.close()
            return ret

        cursor.close()
