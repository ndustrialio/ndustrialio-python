from ndustrialio.apiservices import *

class WorkerService(LegacyService):

    def __init__(self, access_token=None):

        super(WorkerService, self).__init__(access_token=access_token)

    def get(self, id=None, execute=True):

        if id is None:
            uri='workers'
        else:
            uri='workers/'+id

        return self.execute(GET(uri=uri), execute)


    def getConfigurationValues(self, id, environment=None, execute=True):

        params = {}
        if environment is not None:
            params = {'environment': environment}

        return self.execute(GET(uri='/'.join(['workers', id, 'configurations', 'values']))
                            .params(params=params),
                            execute=execute)


    def updateConfigurationValue(self, configuration_id, value_id, key=None, value=None, value_type=None, execute=True):

        params = {}

        if key is not None:
            params['key'] = key

        if value is not None:

            params['value'] = value

        if value_type is not None:

            params['value_type'] = value_type

        return self.execute(PUT(uri='/'.join(
            ['configurations',
            str(configuration_id),
            'values',
            str(value_id)]
            )).body(body=params), execute=execute)

    def createConfigurationValue(self, configuration_id, key, value, value_type, execute=True):

        return self.execute(POST(uri='/'.join(['configurations', str(configuration_id), 'values']))
                            .body(body={'key': key, 'value': value, 'value_type': value_type}),
                            execute=execute)

    def deleteConfigurationValue(self, configuration_id, value_id, execute=True):

        return self.execute(DELETE(
            uri='/'.join[
                'configurations',
                str(configuration_id),
                'values',
                str(value_id)]), execute=execute)