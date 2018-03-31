import requests
import os
import json
from datetime import datetime
import pytz
from tzlocal import get_localzone
from auth0.v2.authentication import Oauth

API_VERSION = 'v1'

BASE_URL = 'http://api.ndustrial.io'

AUTH_URL = 'https://contxtauth.com'
AUTH0_URL = 'ndustrialio.auth0.com'


def delocalize_datetime(dt_object):
    localized_dt = get_localzone().localize(dt_object)
    return localized_dt.astimezone(pytz.utc)


def get_epoch_time(dt_object):
    if dt_object.tzinfo is None:
        # assuming an naive datetime is in the callers timezone
        # as set on the system,
        dt_object = get_localzone().localize(dt_object)

    utc_1970 = datetime(1970, 1, 1).replace(tzinfo=pytz.utc)

    return int((dt_object.astimezone(pytz.utc) - utc_1970).total_seconds())


class ApiClient(object):
    def __init__(self, access_token):

        self.access_token = access_token

    def execute(self, api_request):

        headers = {}
        retries = 3
        status = -1

        response = None

        while status in [-1, 504] and retries > 0:

            # authorize this request?
            if api_request.authorize():
                headers['Authorization'] = 'Bearer ' + self.access_token

            if api_request.method() == 'GET':
                response = requests.get(url=str(api_request), headers=headers)
            if api_request.method() == 'POST':
                if api_request.content_type == ApiRequest.URLENCODED_CONTENT_TYPE:
                    response = requests.post(url=str(api_request), data=api_request.body(), headers=headers)
                else:
                    response = requests.post(url=str(api_request), json=api_request.body(), headers=headers)
            if api_request.method() == 'PUT':
                response = requests.put(url=str(api_request), data=api_request.body(), headers=headers)
            if api_request.method() == 'DELETE':
                response = requests.delete(url=str(api_request), headers=headers)

            status = response.status_code
            retries -= 1

        return self.process_response(response)

    def process_response(self, response):

        # throw an exception in case of a status problem
        # response.raise_for_status()

        # lifted the following code from requests/models.py and modified it
        http_error_msg = ''

        if 400 <= response.status_code < 500:
            msg = json.loads(response.text)['message']
            http_error_msg = '%s Client Error: %s - %s' % (response.status_code, response.reason, msg)

        elif response.status_code == 500:
            msg = json.loads(response.text)['message']
            http_error_msg = '%s Server Error: %s - %s' % (response.status_code, response.reason, msg)

        elif 500 < response.status_code < 600:
            http_error_msg = '%s Server Error: %s - %s' % (response.status_code, response.reason, response.text)

        if http_error_msg:
            raise requests.exceptions.HTTPError(http_error_msg, response=self)

        # decode json response if there is a response
        if response.status_code != 204:
            return response.json()
        else:
            return None


class PagedResponse(object):
    def __init__(self, data):
        self.total_records = data['_metadata']['totalRecords']
        self.offset = data['_metadata']['offset']

        self.records = data['records']

    def first(self):
        return self.records[0]

    def __iter__(self):
        for record in self.records:
            yield record


class DataResponse(object):
    def __init__(self, data, client):
        self.client = client
        self.count = data['meta']['count']
        self.has_more = data['meta']['has_more']

        self.next_page_url = None
        if self.has_more:
            self.next_page_url = data['meta']['next_page_url']

        self.records = data['records']

    def __iter__(self):

        while True:
            for record in self.records:
                record['event_time'] = datetime.strptime(record['event_time'], "%Y-%m-%dT%H:%M:%S.%fZ")
                yield record

            if self.has_more:
                # print 'Requesting more records..'
                response = self.client.execute(StringRequest(self.next_page_url).method('GET'))

                self.count = response['meta']['count']
                self.has_more = response['meta']['has_more']

                self.next_page_url = None
                if self.has_more:
                    self.next_page_url = response['meta']['next_page_url']

                self.records = response['records']
            else:
                break


class StringRequest(object):
    URLENCODED_CONTENT_TYPE = 'application/x-www-form-urlencoded'
    JSON_CONTENT_TYPE = 'application/json'

    def __init__(self, request_string):
        self.request_string = request_string

        # authorize request, default true
        self.authorize_request = True

        self.http_content_type = self.JSON_CONTENT_TYPE

        self.http_body = {}

        self.http_method = None

    def authorize(self, authorize=None):

        if authorize is None:
            return self.authorize_request
        else:
            self.authorize_request = authorize

            return self

    def body(self, body=None):
        if body is None:
            return self.http_body
        else:
            self.http_body = body
            return self

    def content_type(self, content_type=None):

        if content_type is None:
            return self.http_content_type
        else:
            self.http_content_type = content_type
            return self

    def method(self, method=None):
        if method is None:
            return self.http_method
        else:
            self.http_method = method
            return self

    def __str__(self):
        return self.request_string


class ApiRequest(object):
    URLENCODED_CONTENT_TYPE = 'application/x-www-form-urlencoded'
    JSON_CONTENT_TYPE = 'application/json'

    def __init__(self, uri, authorize=True):

        self.uri = uri

        self.http_base_url = None

        # authorize request, default true
        self.authorize_request = authorize

        self.http_content_type = self.JSON_CONTENT_TYPE

        self.http_params = {}

        self.api_version = True

        self.http_method = None

        self.http_body = {}

    def params(self, params=None):

        if params is None:
            return self.http_params
        else:
            self.http_params = params
            return self

    def authorize(self, authorize=None):

        if authorize is None:
            return self.authorize_request
        else:
            self.authorize_request = authorize

            return self

    def base_url(self, base_url=None):
        if base_url is None:
            return self.http_base_url
        else:
            self.http_base_url = base_url

            return self

    def version(self, version=None):

        if version is None:
            return self.api_version
        else:
            self.api_version = version
            return self

    def method(self, method=None):
        if method is None:
            return self.http_method
        else:
            self.http_method = method
            return self

    def content_type(self, content_type=None):

        if content_type is None:
            return self.http_content_type
        else:
            self.http_content_type = content_type
            return self

    def body(self, body=None):
        if body is None:
            return self.http_body
        else:
            self.http_body = body
            return self

    def __str__(self):

        request_chunks = []

        request_chunks.append(self.http_base_url)

        if self.api_version:
            request_chunks.append(API_VERSION)

        request_chunks.append(self.uri)

        # append params
        if self.http_params:
            param_string = '?'

            param_list = []

            for p, v in self.http_params.items():
                param_list.append(p + '=' + str(v))

            param_string += '&'.join(param_list)

            request_string = '/'.join(request_chunks) + param_string

        else:
            request_string = '/'.join(request_chunks)

        return request_string


class GET(ApiRequest):
    def __init__(self, uri, authorize=True):
        super(GET, self).__init__(uri, authorize)

    def method(self, method=None):
        return 'GET'


class POST(ApiRequest):
    def __init__(self, uri, authorize=True):
        super(POST, self).__init__(uri, authorize)

    def method(self, method=None):
        return 'POST'


class PUT(ApiRequest):
    def __init__(self, uri, authorize=True):
        super(PUT, self).__init__(uri, authorize)

    def method(self, method=None):
        return 'PUT'


class DELETE(ApiRequest):
    def __init__(self, uri, authorize=True):
        super(DELETE, self).__init__(uri, authorize)

    def method(self, method=None):
        return 'DELETE'


class ApiService(object):
    def __init__(self):

        self.client = None

    def baseURL(self):

        return BASE_URL

    def execute(self, api_request, execute=True):

        if execute:

            result = self.client.execute(api_request.base_url(self.baseURL()))

            return result

        else:
            return api_request.base_url(self.baseURL())


class AuthService(ApiService):
    def __init__(self, auth_url):
        super(AuthService, self).__init__()
        self.url = auth_url
        self.client = ApiClient(None)

    def baseURL(self):
        return self.url

    def machine_login(self, client_id, client_secret, audience):
        body = {'client_id': client_id,
                'client_secret': client_secret,
                'grant_type': 'client_credentials',
                'audience': audience}

        return self.execute(POST(uri='oauth/token', authorize=False).body(body))


class Service(ApiService):
    def __init__(self, client_id, client_secret=None, enable_legacy_auth=False):

        super(Service, self).__init__()

        if client_secret is None:
            client_secret = os.environ.get('CLIENT_SECRET')

        assert client_secret is not None

        if enable_legacy_auth:
            oauth = Oauth(AUTH0_URL)

            token = oauth.login(client_id=client_id,
                                client_secret=client_secret,
                                audience=self.audience(),
                                grant_type='client_credentials')

        else:
            # need to login to get JWT token
            auth = AuthService(AUTH_URL)

            token = auth.machine_login(client_id=client_id,
                                       client_secret=client_secret,
                                       audience=self.audience())

        self.client = ApiClient(access_token=token['access_token'])

    def audience(self):

        return 'base_audience'


class LegacyService(ApiService):
    def __init__(self, access_token=None):
        super(LegacyService, self).__init__()

        if access_token is None:
            access_token = os.environ.get('ACCESS_TOKEN')

        assert access_token is not None

        self.client = ApiClient(access_token=access_token)

    def baseURL(self):
        return BASE_URL


class BatchService(LegacyService):
    def __init__(self, access_token=None):

        super(BatchService, self).__init__(access_token=access_token)

    def batchRequest(self, requests):

        batch_data = {}

        for request_label, request in requests.iteritems():

            r = {'method': request.method(),
                 'uri': str(request)}

            # attach body.. must be JSON content type
            if r['method'] == 'POST':
                r['body'] = request.body()

            batch_data[request_label] = r

        return self.execute(POST(uri='batch').body(body=batch_data))