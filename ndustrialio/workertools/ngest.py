import json
from ndustrialio.apiservices.ngest import NgestService
import pytz

MAX_MESSAGE_FIELDS = 50
TIMESERIES_TYPE = 'timeseries'


class Message(object):
    def __init__(self, feed_key):
        self.data = {}
        self.size = 0
        self.feed_key = feed_key

    def add_value(self, timestamp, field, value):

        if self.size == MAX_MESSAGE_FIELDS:
            return False

        try:
            field_map = self.data[timestamp]

        except KeyError:
            field_map = {}
            self.data[timestamp] = field_map

        if field not in field_map:
            field_map[field] = {"value": str(value)}
            self.size += 1
        else:
            raise Exception('Field: ' + field + ' already present at timestamp: ' + timestamp)

        return True

    def pre_serialize(self):
        serialize_map = {}
        serialize_map['type'] = TIMESERIES_TYPE
        data_arr = []

        for timestamp, fields in self.data.iteritems():
            data_map = {'timestamp': timestamp,
                        'data': fields}
            data_arr.append(data_map)

        serialize_map['data'] = data_arr
        serialize_map['feedKey'] = self.feed_key
        return serialize_map

    def __str__(self):
        return json.dumps(self.pre_serialize())


class TimeSeries(object):
    def __init__(self, feed_key):
        self.messages = [
            Message(feed_key)]
        self.feed_key = feed_key

    def add_value(self, timestamp, field, value):
        if timestamp.tzinfo is None or timestamp.tzinfo.utcoffset(timestamp) is None:
            raise Exception('Please use timezone-aware datetimes with nGest')

        delocalized = timestamp.astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:%S')

        if not self.messages[-1].add_value(delocalized, field, value):
            self.messages.append(Message(self.feed_key))
            self.messages[-1].add_value(delocalized, field, value)

        return

    def __iter__(self):
        for message in self.messages:
            yield message.pre_serialize()


class Ngest(object):
    def __init__(self, feed_key, feed_token):
        self.feed_key = feed_key
        self.feed_token = feed_token
        self.time_series = TimeSeries(feed_key)

    def add_value(self, timestamp, field, value):
        self.time_series.add_value(timestamp, field, value)

    def send_data(self):
        ngest_service = NgestService()
        for message in self.time_series:
            ngest_service.sendData(self.feed_token, self.feed_key, message)

        self.time_series = TimeSeries(self.feed_key)