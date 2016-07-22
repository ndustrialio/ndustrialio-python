import requests


API_VERSION = 'v1'

BASE_URL = 'http://api.ndustrial.io'


class ApiClient(object):

    def __init__(self, access_token, refresh_token=None, client_id=None, client_secret=None):

        self.access_token = access_token

        if all((refresh_token, client_id, client_secret)):

            self.auto_refresh=True

            # Automatic token refresh enabled!
            self.refresh_token = refresh_token
            self.client_id = client_id
            self.client_secret = client_secret

        else:
            self.auto_refresh=False


    def execute(self, api_request):

        headers = {}

        # authorize this request?
        if api_request.authorize():
            headers['Authorization'] = 'Bearer ' + self.access_token

        if api_request.method() == 'GET':
            response=requests.get(url=str(api_request), params=api_request.params(), headers=headers)
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
    JSON_CONTENT_TYPE = 'application/json';

    def __init__(self, uri):

        self.uri = uri

        self.http_base_url = None

        # authorize request, default true
        self.authorize_request = True

        self.http_content_type=self.JSON_CONTENT_TYPE

        self.http_params=None

        self.api_version = True

        self.http_method = None

        self.http_body = None


    def params(self, params=None):

        if not params:
            return self.http_params
        else:
            self.http_params = params
            return self

    def authorize(self, authorize=None):

        if not authorize:
            return self.authorize_request
        else:
            self.authorize_request = authorize

            return self

    def base_url(self, base_url=None):
        if not base_url:
            return self.http_base_url
        else:
            self.http_base_url = base_url

            return self

    def version(self, version=None):

        if not version:
            return self.api_version
        else:
            self.api_version = version
            return self

    def method(self, method=None):
        if not method:
            return self.http_method
        else:
            self.http_method = method
            return self

    def content_type(self, content_type=None):

        if not content_type:
            return self.http_content_type
        else:
            self.http_content_type = content_type
            return self

    def body(self, body=None):
        if not body:
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

        return '/'.join(request_chunks)


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


class APIService(object):

    def __init__(self, client):

        self.client = client

    def baseURL(self):

        return BASE_URL

    def execute(self, api_request):

        return self.client.execute(api_request.base_url(self.baseURL()))


class ServiceInitializer(object):

    def __init__(self, access_token, refresh_token = None, client_id = None, client_secret = None):

        self.client = ApiClient(access_token=access_token,
                                refresh_token=refresh_token,
                                client_id=client_id,
                                client_secret=client_secret)



    def init_service(self, service_class):

        return service_class(self.client)