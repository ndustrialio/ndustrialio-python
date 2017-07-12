import unittest
import json
import requests
import pytz
from mock import patch
from datetime import datetime
from requests.models import Response
from ndustrialio.apiservices import ApiClient
from ndustrialio.apiservices import ApiRequest
from ndustrialio.apiservices import BatchService
from ndustrialio.apiservices import DataResponse
from ndustrialio.apiservices import delocalize_datetime, get_epoch_time

class TestAPIClient(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestAPIClient, self).__init__(*args, **kwargs)
        self.api_client = ApiClient('fake_access_token')


    def get_test_request(self, method, uri='test/uri', base_url='http://base_url.com', params=None, version=None, body=None, content_type=None):
        request = ApiRequest(uri)
        request.base_url(base_url)
        request.method(method)
        request.params(params)
        request.version(version)
        request.body(body)
        request.content_type(content_type)
        return request

    def get_test_response(self, status_code, content=None, reason=None):
        response = Response()
        response.status_code = status_code
        response._content = content
        response.reason = reason
        return response

# delocalize_datetime should convert timezone unaware datetime object into utc
    @patch('ndustrialio.apiservices.get_localzone')
    def test_delocalize_datetime_tz_unaware(self, mock_get_localzone):
        mock_get_localzone.return_value = pytz.timezone('Africa/Cairo')
        tz_unaware_datetime = datetime(1970, 1, 1)
        self.assertEqual(delocalize_datetime(tz_unaware_datetime), datetime(1969, 12, 31, 22, tzinfo=pytz.utc))

# delocalize_datetime should raise ValueError if input datetime object is timezone aware
    def test_delocalize_datetime_tz_aware(self):
        tz_aware_datetime = datetime(1970, 1, 1, tzinfo=pytz.timezone('Africa/Cairo'))
        self.assertRaises(ValueError, delocalize_datetime, tz_aware_datetime)

# get_epoch_time should return number of seconds since 1/1/70 for timezone aware datetime object
    def test_get_epoch_time_tz_aware(self):
        tz_aware_datetime = datetime(1970, 1, 1, tzinfo=pytz.timezone('Africa/Cairo'))
        self.assertEqual(get_epoch_time(tz_aware_datetime), -7500)

# get_epoch_time should return number of seconds since 1/1/70 for timezone unaware datetime object
    @patch('ndustrialio.apiservices.get_localzone')
    def test_get_epoch_time_tz_unaware(self, mock_get_localzone):
        mock_get_localzone.return_value = pytz.timezone('Africa/Cairo')
        tz_unaware_datetime = datetime(1970, 1, 1)
        self.assertEqual(get_epoch_time(tz_unaware_datetime), -7200)

# ApiClient.execute should format authorization header, if the request needs to be authorized
    @patch.object(requests, 'get')
    @patch.object(ApiClient, 'process_response')
    def test_execute_auth(self, mock_process_response, mock_get):
        mock_process_response.return_value = None
        mock_get.return_value = self.get_test_response(200)
        request = self.get_test_request(method='GET')
        self.api_client.execute(request)
        call_args = mock_get.call_args
        self.assertEqual(call_args[1]['headers']['Authorization'], 'Bearer fake_access_token')

# ApiClient.execute should call requests.get, if the request method is GET
    @patch.object(requests, 'get')
    @patch.object(ApiClient, 'process_response')
    def test_execute_get(self, mock_process_response, mock_get):
        mock_process_response.return_value = None
        mock_get.return_value = self.get_test_response(200)
        request = self.get_test_request(method='GET')
        self.api_client.execute(request)
        mock_get.assert_called_once()

# ApiClient.execute should call requests.post with data field, if the request method is POST and content type is url encoded
    @patch.object(requests, 'post')
    @patch.object(ApiClient, 'process_response')
    def test_execute_post_url(self, mock_process_response, mock_post):
        mock_process_response.return_value = None
        mock_post.return_value = self.get_test_response(200)
        request = self.get_test_request(method='POST',
                                        body={'message': 'test'},
                                        content_type=ApiRequest.URLENCODED_CONTENT_TYPE)
        self.api_client.execute(request)
        call_args = mock_post.call_args
        self.assertEqual(call_args[1]['data'], {'message': 'test'})

# ApiClient.execute should call requests.post with json field, if the request method is POST and content type is json
    @patch.object(requests, 'post')
    @patch.object(ApiClient, 'process_response')
    def test_execute_post_json(self, mock_process_response, mock_post):
        mock_process_response.return_value = None
        mock_post.return_value = self.get_test_response(200)
        request = self.get_test_request(method='POST',
                                        body={'message': 'test'},
                                        content_type=ApiRequest.JSON_CONTENT_TYPE)
        self.api_client.execute(request)
        call_args = mock_post.call_args
        self.assertEqual(call_args[1]['json'], {'message': 'test'})

# ApiClient.execute should call requests.put, if the request method is PUT
    @patch.object(requests, 'put')
    @patch.object(ApiClient, 'process_response')
    def test_execute_put(self, mock_process_response, mock_put):
        mock_process_response.return_value = None
        mock_put.return_value = self.get_test_response(200)
        request = self.get_test_request(method='PUT')
        self.api_client.execute(request)
        mock_put.assert_called_once()

# ApiClient.execute should call requests.delete, if the request method is DELETE
    @patch.object(requests, 'delete')
    @patch.object(ApiClient, 'process_response')
    def test_execute_delete(self, mock_process_response, mock_delete):
        mock_process_response.return_value = None
        mock_delete.return_value = self.get_test_response(200)
        request = self.get_test_request(method='DELETE')
        self.api_client.execute(request)
        mock_delete.assert_called_once()

# ApiClient.execute should retry a minimum of 3 times, if the endpoint returns status code 504
    @patch.object(requests, 'get')
    @patch.object(ApiClient, 'process_response')
    def test_execute_retries(self, mock_process_response, mock_get):
        mock_process_response.return_value = None
        mock_get.return_value = self.get_test_response(504)
        request = self.get_test_request(method='GET')
        self.api_client.execute(request)
        self.assertTrue(len(mock_get.mock_calls) >= 3)
        mock_process_response.assert_called_once()

# ApiClient.process_response should return HTTPError with Client Error message, if response status code is between 400 and 500
    def test_client_error(self):
        response = self.get_test_response(status_code=450,
                                          content=b'{"message": "450_test_message"}',
                                          reason='450_test')
        self.assertRaisesRegexp(requests.exceptions.HTTPError,
                                '450 Client Error: *',
                                self.api_client.process_response,
                                response)

#  ApiClient.process_response should return HTTPError with Server Error message, if response status code is between 500 and 600
    def test_server_error(self):
        response = self.get_test_response(status_code=550,
                                          content=b'{"message": "550_test_message"}',
                                          reason='550_test')
        self.assertRaisesRegexp(requests.exceptions.HTTPError,
                                '550 Server Error: *',
                                self.api_client.process_response,
                                response)

# ApiClient.process_response should return None, if response status code is 204
    def test_204_status(self):
        response = self.get_test_response(status_code=204,
                                          content=b'{"message": "204_test_message"}',
                                          reason='204_test')
        processed_response = self.api_client.process_response(response)
        self.assertTrue(processed_response is None)

# ApiClient.process_response should return response JSON, if response status code is 200
    def test_request_success(self):
        response = self.get_test_response(status_code=200,
                                          content=b'{"key": "value"}')
        processed_response = self.api_client.process_response(response)
        self.assertEqual(processed_response, json.loads(json.dumps({'key': 'value'})))

# DataResponse.__iter__ should continue to execute next requests until there is no more data
    @patch.object(ApiClient, 'execute')
    def test_data_response_iter(self, mock_execute):
        data_first = {'meta':
                          {
                              'count': 2,
                              'has_more': True,
                              'next_page_url': 'http://base_url.com'
                          },
                      'records':
                          [
                              {'event_time': '2015-01-12T00:00:00.000Z'},
                              {'event_time': '2016-01-12T00:00:00.000Z'}
                          ]
                     }
        data_second = {'meta':
                          {
                              'count': 2,
                              'has_more': False,
                              'next_page_url': 'http://base_url.com'
                          },
                      'records':
                          [
                              {'event_time': '2017-01-12T00:00:00.000Z'},
                              {'event_time': '2018-01-12T00:00:00.000Z'}
                          ]
                     }
        mock_execute.return_value = data_second
        data_response = DataResponse(data_first, self.api_client)
        records = []
        for record in data_response:
            records.append(record)
        self.assertEqual(records, [{'event_time': datetime.strptime('2015-01-12T00:00:00.000Z', "%Y-%m-%dT%H:%M:%S.%fZ")},
                                   {'event_time': datetime.strptime('2016-01-12T00:00:00.000Z', "%Y-%m-%dT%H:%M:%S.%fZ")},
                                   {'event_time': datetime.strptime('2017-01-12T00:00:00.000Z', "%Y-%m-%dT%H:%M:%S.%fZ")},
                                   {'event_time': datetime.strptime('2018-01-12T00:00:00.000Z', "%Y-%m-%dT%H:%M:%S.%fZ")}])

# ApiRequest.__str__ should return properly formatted request string
    def test_request_to_string(self):
        request = self.get_test_request(method='GET',
                                        params={'key': 'value'})
        self.assertEqual(str(request), 'http://base_url.com/v1/test/uri?key=value')

# BatchService.batchRequest executes batch request call to /batch uri
    @patch.object(BatchService, 'execute')
    def test_batch_request(self, mock_execute):
        batch_service = BatchService('fake_token')
        mock_execute.return_value = None

        request_one = self.get_test_request(method='GET',
                                            params={'key1': 'value1'},
                                            version='v1')

        request_two = self.get_test_request(method='POST',
                                            version='v2',
                                            body={'body_key': 'body_value'},
                                            content_type='application/json')

        batch_request = {'request_one': request_one,
                          'request_two': request_two}

        batch_service.batchRequest(batch_request)

        call_args = mock_execute.call_args

        self.assertEqual(call_args[0][0].uri, 'batch')
        self.assertEqual(call_args[0][0].http_body, {'request_one':
                                                     {'method': 'GET',
                                                      'uri': 'http://base_url.com/v1/test/uri?key1=value1'},
                                                     'request_two':
                                                     {'body': {'body_key': 'body_value'},
                                                      'method': 'POST',
                                                      'uri': 'http://base_url.com/v1/test/uri'}})

