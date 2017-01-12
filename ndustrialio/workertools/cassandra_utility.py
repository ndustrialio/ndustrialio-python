from cassandra.cluster import Cluster
from cassandra import ConsistencyLevel
from datetime import datetime
import collections
from query import CQLSelect, Where



class CassandraUtility:

    def __init__(self, host, keyspace):

        self.cluster = Cluster([host])

        self.session = self.cluster.connect(keyspace=keyspace)


    def execute(self, query, args=None):

        statement = self.session.prepare(query)

        statement.consistency_level = ConsistencyLevel.TWO

        if args is not None:

            return self.session.execute(statement, args)

        else:

            return self.session.execute(statement)




    def getActiveOutputs(self, output_filter=None, field_filter=None):

        statement = 'SELECT output_id, event_time, field from output_data_by_field_latest'

        data = self.execute(statement)

        now = datetime.utcnow()

        # filter only recent data
        latestData = [ld for ld in data if (now-ld.event_time).days <= 5]


        # filter outputs
        if output_filter:
            latestData = [ld for ld in latestData if ld.output_id in output_filter]

        outputs = {}

        # if there is a field_filter, only include outputs containing fields from the
        # filter
        if field_filter:

            for ld in latestData:

                if ld.field in field_filter:

                    if ld.output_id not in outputs:
                        outputs[ld.output_id] = []

                    outputs[ld.output_id].append(ld.field)

        else:

            for ld in latestData:

                if ld.output_id not in outputs:
                    outputs[ld.output_id] = []

                outputs[ld.output_id].append(ld.field)


        return outputs


    def getData(self, output_id, field_human_name, time_start, window=0, time_end=None, limit=None):

        assert window in [0, 1, 15, 60]

        if window == 0:

            table_name = 'output_data_by_field'

        elif window == 1:

            table_name = 'output_data_by_field_minutely'

        elif window == 15:

            table_name = 'output_data_by_field_15_minutely'

        else:

            table_name = 'output_data_by_field_hourly'




        results = collections.OrderedDict()


        if time_end is not None:

            # need to construct a data structure of single-year timestamp ranges
            years = collections.OrderedDict()

            year = time_start.year

            final_year = time_end.year

            query_start = time_start

            while year <= final_year:

                year_end_date = datetime(year, 12, 31, hour=23, minute=59, second=59, microsecond=int(1e-6-1))


                if time_end < year_end_date:
                    # query ends before current year, use time_end
                    years[year] = (query_start, time_end)

                    # go on to next year
                    year+=1
                else:
                    # year ends before query
                    years[year] = (query_start, year_end_date)

                    # go on to next year
                    year+=1

                    # new query start
                    query_start = datetime(year, 1, 1)




            for year, timestamps in years.iteritems():

                cql = CQLSelect(table_name).fields(['value', 'event_time'])

                cql.where(Where('output_id=?')
                          .AND('field=?')
                          .AND("year='"+str(year)+"'")
                          .AND("event_time>=?")
                          .AND("event_time<=?"))

                cql.order('event_time')

                if limit is not None:
                    cql.limit(limit)


                rows = self.execute(str(cql), [output_id, field_human_name, timestamps[0], timestamps[1]])

                for row in rows:
                    results[row.event_time] = row.value



        else:

            cql = 'SELECT * FROM ' + table_name + " WHERE output_id=? " \
                                        "AND field=? " \
                                        "AND year='"+str(time_start.year)+"' " \
                                        "AND event_time>=? " \
                                        "ORDER BY event_time ASC"



            rows = self.execute(cql, [output_id, field_human_name, time_start])


            for row in rows:

                results[row.event_time] = row.value

        return results


    def putData(self, output_id, field_human_name, window, value, timestamp):

        year = str(timestamp.year)

        assert window in [0, 1, 15, 60]

        if window == 0:

            table_name = 'output_data_by_field'

        elif window == 1:

            table_name = 'output_data_by_field_minutely'

        elif window == 15:

            table_name = 'output_data_by_field_15_minutely'

        else:

            table_name = 'output_data_by_field_hourly'




        cql = 'INSERT INTO ' + table_name + ' (output_id, field, year, event_time, value) ' \
                                                                       ' VALUES(?,?,?,?,?)'


        self.execute(cql, [output_id, field_human_name, year, timestamp, str(value)])


    def deleteData(self, output_id, field_human_name, window, timestamp):

        assert window in [0, 1, 15, 60]

        year = str(timestamp.year)

        if window == 0:

            table_name = 'output_data_by_field'

        elif window == 1:

            table_name = 'output_data_by_field_minutely'

        elif window == 15:

            table_name = 'output_data_by_field_15_minutely'

        else:

            table_name = 'output_data_by_field_hourly'


        cql = 'DELETE FROM ' + table_name + ' WHERE output_id=? and field=? and year=? and event_time=?'

        self.execute(cql, [output_id, field_human_name, year, timestamp])



    def getDateString(self, timestamp):

        month = '%02d' % timestamp.month

        return str(timestamp.year) + '-' + month