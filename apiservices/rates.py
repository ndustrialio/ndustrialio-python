from apiservices import *

class RatesService(Service):

    clientID = 'IhnocBdLJ0UBmAJ3w7HW6CbwlpPKHj2Y'

    def __init__(self, client):

        super(RatesService, self).__init__(client)

    def baseURL(self):

        return 'https://rates.api.ndustrial.io'

    def getSchedules(self, execute=True):

        return self.execute(GET(uri='schedules'), execute)



