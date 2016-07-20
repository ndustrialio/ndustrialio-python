from apiservices import *


class OpsmetricService(APIService):

    BASE_URL = ''

    def __init__(self, client):

        super(OpsmetricService, self).__init__(self, client)


    def getSystems(self):

        return self.client.execute(GET(uri='wms/systems', base_uri=BASE_URL))


    def get_translations(self, wms_system_id, message_path_id):
        pass