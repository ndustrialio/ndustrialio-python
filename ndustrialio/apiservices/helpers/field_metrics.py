from datetime import timedelta
from math import sqrt
from ndustrialio.apiservices import *
from ndustrialio.apiservices.feeds import FeedsService

class FieldMetrics:

    def __init__(self, client_id, client_secret):
        self.feed_service = FeedsService(client_id, client_secret)

    '''
        Main helper method to get field data metrics over a period of time given a time range, an interval between those
        times, and a list of outputs and fields

        Parameters:
        -- start_time_datetime - Start time within the range of time you want metrics
        -- end_time_datetime - End time within the range of time you want metrics
        -- minute_interval - Number of minutes for your bucket size
        -- field_identification_list - List of fields you want to base your metrics on (list of hashmaps
                                        {'output_id': <output_id>,
                                         'field_human_name': <field_human_name>
                                         }

    '''
    def getBatchFieldDataMetrics(self, start_time_datetime, end_time_datetime, minute_interval, field_identification_list):

        if start_time_datetime > end_time_datetime:
            raise Exception('Start time must be less than end time')

        data_request_map = {}
        request_count = 0
        max_batch_requests = 20

        bin_edges = self.getBinEdges(start_time_datetime, end_time_datetime, minute_interval)
        bin_map = {time_tuple: [] for time_tuple in bin_edges}

        for field_identification in field_identification_list:

            if 'output_id' in field_identification:
                output_id = field_identification['output_id']
            else:
                raise Exception('output_id not included in field hashmap')
            if 'field_human_name' in field_identification:
                field_human_name = field_identification['field_human_name']
            else:
                raise Exception('field_human_name not included in field hashmap')

            key = "{}.{}".format(output_id, field_human_name)

            data_request = self.feed_service.getData(output_id=output_id,
                                field_human_name=field_human_name,
                                time_end=end_time_datetime,
                                time_start=start_time_datetime,
                                window=60,
                                limit=1000,
                                execute=False)

            data_request_map[key] = {'method': data_request.method(),
                                     'uri': str(data_request)}

            request_count += 1

            if request_count == max_batch_requests:
                batch_data = self.feed_service.execute(POST(uri='batch').body(data_request_map), execute=True)
                bin_map = self.addRecordsToBins(batch_data, bin_map, bin_edges)
                request_count = 0
                data_request_map = {}

        if data_request_map:
            batch_data = self.feed_service.execute(POST(uri='batch').body(data_request_map), execute=True)
            bin_map = self.addRecordsToBins(batch_data, bin_map, bin_edges)

        bin_map = {edge_tuple: self.convertValuesToFloat(record_list) for edge_tuple, record_list in bin_map.items()}

        return self.calculateMetrics(bin_map)

    '''
        Iterate over the given start and end times to calculate the bin edges given the desired minute interval.
        If the full time range is not a multiple of the time interval, the final bin's end time will equal the end
        time of the time range, and the final bin may be smaller than the time interval.
    '''
    def getBinEdges(self, start_time_datetime, end_time_datetime, minute_interval):

        time_range_minutes = divmod((end_time_datetime - start_time_datetime).total_seconds(), 60)[0]
        interval_timedelta = timedelta(minutes=minute_interval)

        if minute_interval > time_range_minutes:
            raise Exception('Time interval should not be larger than the time range')

        # Array of (start_time, end_time) datetime tuples labeling the edges of each bin
        # For each value x in a given bin with (start_time, end_time), start_time <= x < end_time

        bin_edges = []
        current_start_time_datetime = start_time_datetime

        while True:
            if (current_start_time_datetime + interval_timedelta) > end_time_datetime:
                bin_edges.append(tuple([current_start_time_datetime, end_time_datetime]))
                break
            else:
                bin_edges.append(tuple([current_start_time_datetime, current_start_time_datetime + interval_timedelta]))
                current_start_time_datetime += interval_timedelta

        return bin_edges

    '''
        Add the response of a batch request for raw data to the bin map.
        For a bin with edges (start, end), all values x in the bin must be start <= x < end
    '''
    def addRecordsToBins(self, batch_data, bin_map, bin_edges):

        for key, value in batch_data.items():

            records = value['body']['records']
            reversed_records = reversed(records)
            bin_edges_index = 0
            current_time_tuple = bin_edges[bin_edges_index]
            current_end_time = current_time_tuple[1]
            current_list = bin_map[current_time_tuple]

            for record in reversed_records:
                event_time_datetime = datetime.strptime(record['event_time'], "%Y-%m-%dT%H:%M:%S.%fZ")

                if event_time_datetime >= current_end_time:
                    bin_edges_index += 1
                    if bin_edges_index == len(bin_edges):
                        current_list.append(record)
                        bin_map[current_time_tuple] = current_list
                        break
                    else:
                        bin_map[current_time_tuple] = current_list
                        current_time_tuple = bin_edges[bin_edges_index]
                        current_end_time = current_time_tuple[1]
                        current_list = bin_map[current_time_tuple]
                        current_list.append(record)
                else:
                    current_list.append(record)

            bin_map[current_time_tuple] = current_list

        return bin_map

    '''
        Convert the value of each record in a list into a float, or throw the record away if it is not valid
    '''
    def convertValuesToFloat(self, record_list):

        new_list = []

        if record_list:
            for record in record_list:
                value = None

                try:
                    value = float(record['value'])
                except KeyError:
                    print ('Warning: Record: {} does not have value field'.format(record))
                except ValueError:
                    print ('Warning: Value: {} can not be converted to float type'.format(record['value']))

                if value:
                    new_list.append(value)

        return new_list

    '''
        Calculate the metrics we're trying to grab.
        Return result in format {(start_datetime_0, end_datetime_0):
                                    {'minimum: min_value,
                                     'maximum: max_value,
                                     'mean': mean_value,
                                     'standard_deviation': standard_deviation_value
                                     }
                                 (start_datetime_1, end_datetime_1):
                                    ...
                                }
    '''
    def calculateMetrics(self, bin_map):

        return {edge_tuple: {
                    'minimum': self.calculate_minimum(value_list),
                    'maximum': self.calculate_maximum(value_list),
                    'mean': self.calculate_mean(value_list),
                    'standard_deviation': self.calculate_stdev(value_list)
                    }
                for edge_tuple, value_list in bin_map.items()
        }

    def calculate_minimum(self, list):

        minimum = None

        try:
            minimum = min(list)
        except:
            print("Could not find minimum of list: {}".format(list))

        return minimum

    def calculate_maximum(self, list):

        maximum = None

        try:
            maximum = max(list)
        except:
            print("Could not find maximum of list: {}".format(list))

        return maximum

    def calculate_mean(self, list):

        mean = None

        try:
            mean = sum(list)/len(list)
        except:
            print("Could not find mean of list: {}".format(list))

        return mean

    def calculate_stdev(self, list):

        stdev = None

        try:
            stdev = self.standard_deviation(list)
        except:
            print("Could not find standard deviation of list: {}".format(list))

        return stdev

    def standard_deviation(self, list):

        num_items = len(list)
        mean = sum(list) / num_items
        differences = [x - mean for x in list]
        sq_differences = [d ** 2 for d in differences]
        ssd = sum(sq_differences)
        variance = ssd / (num_items - 1)
        sd = sqrt(variance)

        return sd