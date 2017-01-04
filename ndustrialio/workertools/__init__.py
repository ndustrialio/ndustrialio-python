import json
import os

from ndustrialio.apiservices.contxt import ContxtService


class BaseWorker(object):
    def __init__(self, client_id, environment, client_secret=None):
        self.env = environment
        self.client_id = client_id
        self.contxt = ContxtService(client_id, client_secret)
        self.configuration_id = None
        self.run_id = None

        # load configuration
        self.config = self.loadConfiguration()

    def startWorker(self):
        self.run_id = self.contxt.startWorkerRun()
        self.doWork()
        self.contxt.endWorkerRun(self.run_id)

    def addMetric(self, key, value):
        self.contxt.addWorkerRunMetric(self.run_id, key, value)

    def loadConfiguration(self):
        configValues = self.contxt.getConfigurationByClient(self.env)
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