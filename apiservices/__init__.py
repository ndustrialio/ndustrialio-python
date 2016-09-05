import requests
import os
from auth0.v2.authentication import Oauth



API_VERSION = 'v1'

BASE_URL = 'http://api.ndustrial.io'

AUTH0_URL = 'ndustrialio.auth0.com'


class ApiClient(object):

    def __init__(self, access_token):

        self.access_token = access_token

    def execute(self, api_request):

        headers = {}

        # authorize this request?
        if api_request.authorize():
            headers['Authorization'] = 'Bearer ' + self.access_token

        if api_request.method() == 'GET':
            response=requests.get(url=str(api_request), headers=headers)
        if api_request.method() == 'POST':
            if api_request.content_type == ApiRequest.URLENCODED_CONTENT_TYPE:
                response = requests.post(url=str(api_request), data=api_request.body(), headers=headers)
            else:
                response = requests.post(url=str(api_request), json=api_request.body(), headers=headers)
        if api_request.method() == 'PUT':
            response=requests.put(url=str(api_request), data=api_request.body(), headers=headers)
        if api_request.method() == 'DELETE':
            response=requests.delete(url=str(api_request), headers=headers)

        return self.process_response(response)

    def process_response(self, response):

        # throw an exception in case of a status problem
        response.raise_for_status()

        # decode json response if there is a response
        if response.status_code != 204:
            return response.json()
        else:
            return None


class ApiRequest(object):

    URLENCODED_CONTENT_TYPE = 'application/x-www-form-urlencoded'
    JSON_CONTENT_TYPE = 'application/json'

    def __init__(self, uri):

        self.uri = uri

        self.http_base_url = None

        # authorize request, default true
        self.authorize_request = True

        self.http_content_type=self.JSON_CONTENT_TYPE

        self.http_params={}

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
            param_string='?'

            param_list = []

            for p, v in self.http_params.iteritems():
                param_list.append(p+'='+str(v))

            param_string += '&'.join(param_list)

            request_string = '/'.join(request_chunks) + param_string

        else:
            request_string = '/'.join(request_chunks)

        return request_string


class GET(ApiRequest):

    def __init__(self, uri):

        super(GET, self).__init__(uri)

    def method(self, method=None):

        return 'GET'

class POST(ApiRequest):

    def __init__(self, uri):

        super(POST, self).__init__(uri)

    def method(self, method=None):

        return 'POST'

class PUT(ApiRequest):

    def __init__(self, uri):

        super(PUT, self).__init__(uri)

    def method(self, method=None):

        return 'PUT'

class DELETE(ApiRequest):

    def __init__(self, uri):

        super(DELETE, self).__init__(uri)

    def method(self, method=None):

        return 'DELETE'


class ApiService(object):

    def __init__(self, client):

        self.client = client

    def baseURL(self):

        return BASE_URL

    def execute(self, api_request, execute=True):

        if execute:

            result = self.client.execute(api_request.base_url(self.baseURL()))

            return result

        else:
            return api_request.base_url(self.baseURL())


class Service(ApiService):
    def __init(self, client):

        super(Service, self).__init__(client)

class LegacyService(ApiService):

    def __init__(self, client):

        super(LegacyService, self).__init__(client)


class ServiceInitializer(object):

    @staticmethod
    def init_service(service_class, client_id=None):

        assert ((service_class.__base__ == Service) or (service_class.__base__ == LegacyService))

        if (service_class.__base__ == Service):

            # modern auth0 service

            # need a client ID to do this
            assert client_id != None

            # need to login to get JWT token
            oauth = Oauth(AUTH0_URL)

            token = oauth.login(client_id=client_id,
                                client_secret=os.environ.get('CLIENT_SECRET'),
                                audience=service_class.clientID,
                                grant_type='client_credentials')

            return service_class(ApiClient(access_token=token['access_token']))

        else:
            # legacy service.. grab access token from environment
            return service_class(ApiClient(access_token=os.environ.get('ACCESS_TOKEN')))





class BatchService(LegacyService):

    def __init__(self, client):

        super(BatchService, self).__init__(client)


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