from apiservices import *

class RatesService(Service):

    def __init__(self, client_id, client_secret=None):

        super(RatesService, self).__init__(client_id, client_secret)

    def baseURL(self):

        return 'https://rates.api.ndustrial.io'

    def audience(self):

        return 'IhnocBdLJ0UBmAJ3w7HW6CbwlpPKHj2Y'

    def getSchedules(self, execute=True):

        return self.execute(GET(uri='schedules'), execute)

    def getSchedulePeriods(self, id, execute=True):
        
        return self.execute(GET(uri='schedules/{}/periods'.format(id)), execute)
    
    def getPeriod(self, id, execute=True):
        
        return self.execute(GET(uri='periods/{}'.format(id)), execute)

