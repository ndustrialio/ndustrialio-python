from ndustrialio.apiservices import *
from datetime import datetime


class ContxtService(Service):
    def __init__(self, client_id, client_secret=None):
        self.client_id = client_id
        super(ContxtService, self).__init__(client_id, client_secret)

    def baseURL(self):
        return 'https://contxt.api.ndustrial.io'

    def audience(self):
        return '8qY2xJob1JAxhmVhIDLCNnGriTM9bct8'

    def getConfigurationByClient(self, environment_id, execute=True):
        return self.execute(
            GET(uri='clients/{}/configurations?environment_id={}'.format(self.client_id, environment_id)), execute)

    def startWorkerRun(self, execute=True):
        return self.execute(POST(uri='clients/{}/runs'.format(self.client_id))
                            .body(body={'start_time': str(datetime.now())}),
                            execute=execute)

    def endWorkerRun(self, run_id, execute=True):
        return self.execute(PUT(uri='clients/{}/runs/{}'.format(self.client_id, run_id))
                            .body(body={'end_time': str(datetime.now())}),
                            execute=execute)

    def addWorkerRunMetric(self, run_id, key, value, execute=True):
        return self.execute(POST(uri='runs/{}/metrics'.format(run_id))
                            .body(body={'key': str(key), 'value': str(value)}),
                            execute=execute)

