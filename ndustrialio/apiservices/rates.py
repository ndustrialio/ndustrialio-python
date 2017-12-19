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
        
    def getScheduleInfo(self, rate_schedule_id, execute=True):
        
        assert isinstance(rate_schedule_id, int)
        
        return self.execute(GET(uri='/schedules/{}'.format(rate_schedule_id)), execute)
    
    def getScheduleRTPPeriods(self, id, orderBy=None, reverseOrder=False, execute=True):
        
        params = {}
        if orderBy:
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
        assert isinstance(id, int)
        assert isinstance(timeStart, datetime)
        assert isinstance(timeEnd, datetime)
        if timeStart.tzinfo is None or timeEnd.tzinfo is None:
            raise ValueError('timeStart and timeEnd must be tz aware')

        # split the times up into regions avoiding year boundaries
        # e.g [(timeEnd, EndofYear1), (StartofYear2, EndofYear2), (StartofYear3, timeEnd)]
        EoY = timeStart.replace(month=12, day=31, hour=23, minute=59, second=59)
        timeBoundaries = [(timeStart, min(timeEnd,EoY))]
        while timeBoundaries[-1][1] != timeEnd:
            EoY = EoY.replace(year=EoY.year+1)
            SoY = EoY.replace(month=1, day=1, hour=0, minute=0, second=0)
            timeBoundaries.append((SoY, min(timeEnd,EoY)))

        # combine all calls into one. offset is set to 0
        data = dict(_meta=dict(count=0, offset=0), records=[])
        params = {}
        for times in timeBoundaries:
            params['timeStart'] = get_epoch_time(times[0])
            params['timeEnd'] = get_epoch_time(times[1])
            d = self.execute(GET(uri='schedules/{}/usage/periods'.format(id)).params(params), execute)
            data['records'].extend(d['records'])
            data['_meta']['count'] += d['_meta']['count']
        return data
    '''
        Get all demand periods for a range of time
        
        Params:
        id (int) - the rate schedule id
        timeStart (datetime) - start of the time range
        timeEnd (datetime) - end of the time range
        season_type (str) - season type for demand (tou or flat)
    '''
    def getDemandPeriods(self, id, timeStart, timeEnd, season_type=None, execute=True):
        assert isinstance(id, int)
        assert isinstance(timeStart, datetime)
        assert isinstance(timeEnd, datetime)
        if timeStart.tzinfo is None or timeEnd.tzinfo is None:
            raise ValueError('timeStart and timeEnd must be tz aware')

        # split the times up into regions avoiding year boundaries
        # e.g [(timeEnd, EndofYear1), (StartofYear2, EndofYear2), (StartofYear3, timeEnd)]
        EoY = timeStart.replace(month=12, day=31, hour=23, minute=59, second=59)
        timeBoundaries = [(timeStart, min(timeEnd, EoY))]
        while timeBoundaries[-1][1] != timeEnd:
            EoY = EoY.replace(year=EoY.year + 1)
            SoY = EoY.replace(month=1, day=1, hour=0, minute=0, second=0)
            timeBoundaries.append((SoY, min(timeEnd, EoY)))

        params = {}
        if season_type is not None:
            assert isinstance(season_type, str)
            params['season_type'] = season_type

        # combine all calls into one. offset is set to 0
        data = dict(_meta=dict(count=0, offset=0), records=[])
        for times in timeBoundaries:
            params['timeStart'] = get_epoch_time(times[0])
            params['timeEnd'] = get_epoch_time(times[1])
            d = self.execute(GET(uri='schedules/{}/demand/periods'.format(id)).params(params), execute)
            data['records'].extend(d['records'])
            data['_meta']['count'] += d['_meta']['count']
        
        return data
    
    def getRTPPeriod(self, id, execute=True):
        
        return self.execute(GET(uri='rtp/periods/{}'.format(id)), execute)