from ndustrialio.apiservices import *


class OpsmetricService(LegacyService):


    def __init__(self, access_token=None):

        super(OpsmetricService, self).__init__(access_token=access_token)

    def baseURL(self):
        return 'http://opsmetric-translations.api.ndustrial.io'

    def getSystems(self, execute=True):

        return self.execute(GET(uri='wms/systems'), execute)

    def getPaths(self, execute=True):

        return self.execute(GET(uri='wms/paths'), execute)

    def getFields(self, path_id=None, execute=True):

        if path_id is None:
            uri = 'wms/fields'
        else:
            uri = 'wms/paths/'+str(path_id)+'/fields'

        return self.execute(GET(uri=uri), execute)

    def getField(self, field_id, execute=True):

        return self.execute(GET(uri='wms/fields/'+str(field_id)), execute)

    def getTranslations(self, wms_system_id, path_id, execute=True):

        return self.execute(
            GET(uri='wms/systems/'+str(wms_system_id)+'/paths/'+str(path_id)+'/translations'), execute)