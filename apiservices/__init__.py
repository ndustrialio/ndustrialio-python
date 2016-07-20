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

    def __init__(self, uri, base_url=None):

        self.uri = uri

        if base_url is None:
            self.base_url = BASE_URL
        else:
            self.base_url = base_url

        # authorize request, default true
        self.auth = True

        self.content_type=self.JSON_CONTENT_TYPE

        self.params=None

        self.version = True

        self.method = None

        self.body = None


    def params(self, params=None):

        if not params:
            return self.params
        else:
            self.params = params
            return self

    def authorize(self, authorize=None):

        if not authorize:
            return self.auth
        else:
            self.auth = authorize

            return self

    def version(self, version=None):

        if not version:
            return self.version
        else:
            self.version = version
            return self

    def method(self, method=None):
        if not method:
            return self.method
        else:
            self.method = method
            return self

    def content_type(self, content_type=None):

        if not content_type:
            return self.content_type
        else:
            self.content_type = content_type
            return self

    def body(self, body=None):
        if not body:
            return self.body
        else:
            self.body = body
            return self

    def __str__(self):

        request_chunks = []

        request_chunks.append(self.base_url)

        if self.version:
            request_chunks.append(API_VERSION)

        request_chunks.append(self.uri)

        return '/'.join(request_chunks)


class GET(ApiRequest):

    def __init__(self, uri, base_uri=None):

        super(GET, self).__init__(uri, base_uri)

    def method(self, method=None):

        return 'GET'

class POST(ApiRequest):

    def __init__(self, uri, base_uri=None):

        super(POST, self).__init__(uri, base_uri)

    def method(self, method=None):

        return 'POST'

class PUT(ApiRequest):

    def __init__(self, uri, base_uri=None):

        super(PUT, self).__init__(uri, base_uri)

    def method(self, method=None):

        return 'PUT'

class DELETE(ApiRequest):

    def __init__(self, uri, base_uri=None):

        super(DELETE, self).__init__(uri, base_uri)

    def method(self, method=None):

        return 'DELETE'

class APIService(object):

    def __init__(self, client):

        self.client = client


class ServiceInitializer(object):

    def __init__(self, access_token, refresh_token = None, client_id = None, client_secret = None):

        self.client = ApiClient(access_token=access_token,
                                refresh_token=refresh_token,
                                client_id=client_id,
                                client_secret=client_secret)



    def init_service(self, service_class):

        return service_class(self.client)