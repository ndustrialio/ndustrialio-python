from ndustrialio.apiservices import Service, POST

class NgestService(Service):

    def __init__(self):

        super(NgestService, self).__init__(access_token='none')

    def baseURL(self):
        return 'https://data.ndustrial.io'

    def sendData(self, feedToken, feedKey, data, execute=True):
        return self.execute(POST(uri='{}/ngest/{}'.format(feedToken, feedKey))
                            .body(data).authorize(False), execute=execute)