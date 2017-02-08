from ndustrialio.apiservices import *
from datetime import datetime

class RatesService(Service):

    def __init__(self, client_id, client_secret=None):

        super(RatesService, self).__init__(client_id, client_secret)

    def baseURL(self):

        return 'https://rates.api.ndustrial.io'

    def audience(self):

        return 'IhnocBdLJ0UBmAJ3w7HW6CbwlpPKHj2Y'

    def getSchedules(self, execute=True):

        return self.execute(GET(uri='schedules'), execute)

    def getScheduleRTPPeriods(self, id, orderBy=None, reverseOrder=False, execute=True):
        
        params = {}
        if  orderBy:
            assert isinstance(orderBy, str)
            params['orderBy'] = orderBy
        assert isinstance(reverseOrder, bool)
        params['reverseOrder'] = reverseOrder
        
        return self.execute(GET(uri='schedules/{}/rtp/periods'.format(id)).params(params), execute)
    
    '''
        Get all usage periods for a range of time
        
        Params:
        id (int) - the rate schedule id
        timeStart (datetime) - start of the time range
        timeEnd (datetime) - end of the time range
    '''
    def getUsagePeriods(self, id, timeStart, timeEnd, execute=True):
        
        params = {}
        assert isinstance(id, int)
        assert isinstance(timeStart, datetime)
        assert isinstance(timeEnd, datetime)
        params['timeEnd'] = timeEnd.strftime('%s')
        params['timeStart'] = timeStart.strftime('%s')
        
        return self.execute(GET(uri='schedules/{}/usage/periods'.format(id)).params(params), execute)
    
    '''
        Get all demand periods for a range of time
        
        Params:
        id (int) - the rate schedule id
        timeStart (datetime) - start of the time range
        timeEnd (datetime) - end of the time range
    '''
    def getDemandPeriods(self, id, timeStart, timeEnd, execute=True):
        
        params = {}
        assert isinstance(id, int)
        assert isinstance(timeStart, datetime)
        assert isinstance(timeEnd, datetime)
        params['timeEnd'] = timeEnd.strftime('%s')
        params['timeStart'] = timeStart.strftime('%s')
        
        return self.execute(GET(uri='schedules/{}/demand/periods'.format(id)).params(params), execute)
    
    def getRTPPeriod(self, id, execute=True):
        
        return self.execute(GET(uri='rtp/periods/{}'.format(id)), execute)

