from datetime import datetime

from ndustrialio.apiservices import *


class FacilityService(LegacyService):

    def __init__(self, access_token=None):

        super(FacilityService, self).__init__(access_token=access_token)

    def get(self, id=None, execute=True):

        if id is None:
            uri='facilities'
        else:
            uri='facilities/'+str(id)

        return self.execute(GET(uri=uri), execute)

    def getInfo(self, id, execute=True):

        return self.execute(GET(uri='/'.join(['facilities', str(id), 'info'])), execute)


    def getBudget(self, id, execute=True):

        return self.execute(GET(uri='/'.join(['facilities', str(id), 'budget'])), execute)

    def getActualHighs(self, id, start_date, end_date, execute=True):

        assert isinstance(start_date, datetime)
        assert isinstance(end_date, datetime)

        start_str = start_date.strftime('%Y%m%d')
        end_str = end_date.strftime('%Y%m%d')

        return self.execute(GET(uri='/'.join(['facilities', str(id), 'weather', 'actualhighs']))
                            .params({'dateStart': start_str,
                                     'dateEnd': end_str}), execute=execute)

    def getEnergyStartMetrics(self, id, year=None, month=None, execute=True):

        params = {}

        if year is not None and month is not None:
            params['year'] = str(year)
            params['month'] = str(month)

        return self.execute(GET(uri='/'.join(['facilities', str(id), 'metrics', 'energystar']))
                            .params(params), execute=execute)

    def getAccountSummary(self, id, service_type, execute=True):

        return self.execute(GET(uri='/'.join(['facilities', str(id), 'utilities', 'accountsummary']))
                            .params({'service_type': service_type}), execute=execute)

