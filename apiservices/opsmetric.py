from apiservices import *


class OpsmetricService(APIService):


    def __init__(self, client):

        super(OpsmetricService, self).__init__(client)

    def baseURL(self):
        return 'http://opsmetric-translations.api.ndustrial.io'

    def getSystems(self):

        return self.execute(GET(uri='wms/systems'))

    def getPaths(self):

        return self.execute(GET(uri='wms/paths'))

    def getFields(self, path_id=None):

        if path_id is None:
            uri = 'wms/fields'
        else:
            uri = 'wms/paths/'+str(path_id)+'/fields'

        return self.execute(GET(uri=uri))

    def getField(self, field_id):

        return self.execute(GET(uri='wms/fields/'+str(field_id)))

    def getTranslations(self, wms_system_id, path_id):

        return self.execute(
            GET(uri='wms/systems/'+str(wms_system_id)+'/paths/'+str(path_id)+'/translations'))