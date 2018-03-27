import json
import os


from ndustrialio.apiservices.contxt import ContxtService


class ConfiguredComponent(object):
    def __init__(self):

        self.config = None

    def loadConfiguration(self):
        raise NotImplementedError('Cannot directly instantiate ConfiguredComponent')

    def getConfigurationValue(self, key):

        try:
            return self.config[key]['value']

        except KeyError:
            return None


class BaseWorker(ConfiguredComponent):
    def __init__(self, environment, client_id=None, client_secret=None):

        super(BaseWorker, self).__init__()

        self.env = environment

        if client_id is None:
            client_id = os.environ.get("CLIENT_ID")

        assert client_id is not None

        self.client_id = client_id
        self.contxt = ContxtService(client_id, client_secret)
        self.configuration_id = None
        self.run_id = None
        self.config = self.loadConfiguration()

    def startWorker(self):

        run = self.contxt.startWorkerRun()
        print('Worker run ID: '+ run['id'])
        self.run_id = run['id']
        self.doWork()
        self.contxt.endWorkerRun(self.run_id)

    def doWork(self):
        raise NotImplementedError('Must subclass BaseWorker and define doWork')

    def addMetric(self, key, value):
        self.contxt.addWorkerRunMetric(self.run_id, key, value)

    def loadConfiguration(self):
        configValues = self.contxt.getConfigurationByClient(self.env)
        config = {}

        self.configuration_id = configValues['id']

        for value in configValues['ConfigurationValues']:

            configValue = {}

            # store type
            configValue['type'] = value['type']

            # store value
            if configValue['type'] == "integer":
                configValue['value'] = int(value['value'])
            elif configValue['type'] == "json":
                configValue['value'] = json.loads(value['value'])
            else:
                configValue['value'] = str(value['value'])

            # store id
            configValue['id'] = value['id']

            # store config dict
            config[value['key']] = configValue

        return config

    def updateConfigurationValue(self, key, value, value_type=None, is_hidden=False):

        new_val = {'value': value, 'is_hidden':is_hidden}

        if value_type:
            new_val['type'] = value_type

        # update local value
        self.config[key] = new_val

        self.contxt.putConfigurationValue(self.configuration_id, {key:new_val})


    def deleteConfigurationValue(self, key):

        self.contxt.deleteConfigurationValue(self.configuration_id, key)

        # TODO: API provides no way of checking if deletion was successful
        del self.config[key]



class TestWorker(ConfiguredComponent):

    def __init__(self):

        super(TestWorker, self).__init__()

        self.config = self.loadConfiguration()

    def loadConfiguration(self):

        config = {}

        with open('config.json') as config_data:

            config_data = json.loads(config_data.read())

            for config_key, config_value in config_data.iteritems():

                if isinstance(config_value, dict):

                    for k, v in config_value.iteritems():

                        config['-'.join([config_key, k])] = {'value': v}

                else:
                    config[config_key] = config_value

        return config








