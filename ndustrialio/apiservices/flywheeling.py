from ndustrialio.apiservices import *

class FlywheelingService(Service):

    def __init__(self, client_id, client_secret=None):

        super(FlywheelingService, self).__init__(client_id, client_secret)

    def baseURL(self):

        return 'https://flywheeling.api.ndustrial.io'

    def audience(self):

        return 'GvjVT0O7PO1biyzABeqInlodVbN9TsCf'

    def getFacilities(self, execute=True):
        return self.execute(GET(uri='facilities'), execute)
    
    def getSystem(self, system_id, execute=True):
        return self.execute(GET(uri='systems/{}'.format(system_id)), execute)
    
    def getSystemsForFacility(self, facility_id, execute=True):
        return self.execute(GET(uri='facilities/{}/systems'.format(facility_id)), execute)
        
    def getZonesForSystem(self, system_id, execute=True):
        return self.execute(GET(uri='systems/{}/zones'.format(system_id)), execute)
    
    def createRun(self, run_obj):
        return self.execute(POST(uri='runs').body(run_obj))
        
    def addDataToRun(self, run_id, run_data):
        return self.execute(POST(uri='runs/{}/data'.format(run_id)).body(run_data))
    
    def getFacilityAreas(self, facility_id, execute=True):
        return self.execute(GET(uri='facilities/{}/areas'.format(facility_id)), execute)
    
    def addSensorToArea(self, area_id, sensor_id, execute=True):
        return self.execute(POST(uri='areas/{}/sensors/{}'.format(area_id, sensor_id)))

    def getSensorsForArea(self, area_id,limit=10, offset=0, execute=True):
        params = {'limit': limit,
                  'offset': offset}
                  
        return PagedResponse(self.execute(GET(uri='areas/{}/sensors'.format(area_id)).params(params), execute))
    
    ## Scheme-based run
    def createRunForZone(self, zone_id, run_obj):
        
        assert isinstance(zone_id, str)
        assert isinstance(run_obj, dict)
        return self.execute(POST(uri='/zones/{}/runs'.format(zone_id)).body(run_obj))
    
    ## Scheme-based run data
    def addDataToZoneRun(self, run_id, run_data):
        
        assert isinstance(run_id, int)
        assert isinstance(run_data, dict)
        return self.execute(POST(uri='schemes/runs/{}/data'.format(run_id)).body(run_data))
    
    def getSystemSetpointData(self, system_id, execute=True):
        assert isinstance(system_id, str)
        return self.execute(GET(uri='systems/{}/schemes/data'.format(system_id)), execute)

    ## Zone runes
    def getRunsForZone(self, zone_id, orderBy=None, reverseOrder=False, execute=True):
        assert isinstance(zone_id, str)
        params = {}
        if orderBy:
            assert isinstance(orderBy, str)
            params['orderBy'] = orderBy
        if reverseOrder:
            assert isinstance(reverseOrder, bool)
        params['reverseOrder'] = reverseOrder
        return PagedResponse(self.execute(GET(uri='zones/{}/runs'.format(zone_id)).params(params), execute))

    def getLatestRunForZone(self, zone_id):
        params = {'latest': True}
        result = self.execute(GET(uri='zones/{}/runs'.format(zone_id)).params(params), True)
        if (result["records"]) > 0:
            return result["records"][0]
        else:
            return None

    ## Run output
    def getOutputDataForRun(self, run_id, execute=True):
        assert isinstance(run_id, int)
        return self.execute(GET(uri='runs/{}/output'.format(run_id)), execute)

    def addOutputForRun(self, run_id, data_obj):
        assert isinstance(run_id, int)
        if not (isinstance(data_obj, dict) or isinstance(data_obj, list)):
            raise AssertionError("Must pass in a dictionary or list to be formatted into json")

        dataDict = {"data": data_obj}
        return self.execute(POST(uri='runs/{}/output'.format(run_id)).body(dataDict))

    def removeOutputForRun(self, run_id, execute=True):
        assert isinstance(run_id, int)
        return self.execute(DELETE(uri='runs/{}/output'.format(run_id)), execute)
    
    