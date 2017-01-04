from ndustrialio.apiservices import *

class WeatherService(Service):

    def init(self, client_id, client_secret=None):

        super(WeatherService, self).__init__(client_id, client_secret)

    def baseURL(self):
        return 'https://weather.api.ndustrial.io'

    def audience(self):
        return 'cFhOshImtabrVBHzPtwtOLYOT2Mp8IAh'

    def getForecast(self, location_id, execute=True):

        assert isinstance(location_id, int)

        return self.execute(GET(uri='locations/{}/forecast/daily'.format(location_id)), execute=True)

