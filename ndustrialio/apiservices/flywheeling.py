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