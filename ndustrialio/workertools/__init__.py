import json
import os

from ndustrialio.apiservices.contxt import ContxtService


class BaseWorker(object):
    def __init__(self, environment, client_id=None, client_secret=None):
        self.env = environment

        if client_id is None:
            client_id = os.environ.get("CLIENT_ID")

        assert client_id is not None

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

    def updateConfigurationValue(self, key, value, value_type=None, is_hidden=False):

        new_val = {'value': value, 'is_hidden':is_hidden}

        if value_type:
            new_val['value_type'] = value_type

        # update local value
        self.config[key] = new_val

        self.contxt.putConfigurationValue(self.configuration_id, {key:new_val})

    def getConfigurationValue(self, key):

        try:
            return self.config[key]['value']

        except KeyError:
            return None

    def deleteConfigurationValue(self, key):

        self.contxt.deleteConfigurationValue(self.configuration_id, key)

        # TODO: API provides no way of checking if deletion was successful
        del self.config[key]