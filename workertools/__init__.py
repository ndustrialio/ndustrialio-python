from apiservices import ServiceInitializer
from apiservices.workers import WorkerService
import os
import json


class BaseWorker(object):
    def __init__(self, workerID, environment):
        self.env = environment
        self.uuid = workerID
        self.initializer = ServiceInitializer(access_token=os.environ.get('ACCESS_TOKEN'))
        self.workerService = self.initializer.init_service(WorkerService)
        self.configuration_id = None

        # load configuration
        self.config = self.loadConfiguration()

    def loadConfiguration(self):
        self.worker = self.workerService.get(uuid=self.uuid)
        print (self.worker['label'])
        configValues = self.workerService.getConfigurationValues(id=self.uuid, environment=self.env)
        config = {}

        for value in configValues:

            configValue = {}

            # store type
            configValue['type'] = value['type']

            # store value
            if configValue['type'] == "integer":
                configValue['value'] = int(value['value'])
            elif value.type == "json":
                configValue['value'] = json.loads(value['value'])
            else:
                configValue['value'] = str(value['value'])

            # store id
            configValue['id'] = value['id']

            # store config dict
            config[value['key']] = configValue

            # save configuration_id
            # should be the same each time
            # dumb, but whatever
            self.configuration_id = value.configuration_id

        return config

    def updateConfigurationValue(self, key, value):

        # update local value
        configValue = self.config[key]

        configValue['value'] = value

        # send along type so update completes properly
        value_type = configValue['type']

        value_id = configValue['id']

        self.workerService.updateConfigurationValue(self.configuration_id,
                                                    value_id, key=None, value=value,
                                                    value_type=value_type)

    def getConfigurationValue(self, key):

        try:
            return self.config[key]['value']

        except KeyError:
            return None

    def createConfigurationValue(self, key, value, value_type):

        res = self.workerService.createConfigurationValue(self.configuration_id, key, value, value_type)

        # load local values
        configValue = {'value': value, 'id': res.id, 'type': value_type}

        self.config[key] = configValue

    def deleteConfigurationValue(self, key, value):

        self.workerService.deleteConfigurationValue(self.configuration_id, value['id'])

        # TODO: API provides no way of checking if deletion was successful
        del self.config[key]