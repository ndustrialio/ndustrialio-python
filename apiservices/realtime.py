from apiservices import *

class RealtimeService(Service):


    def __init__(self, client):
        super(RealtimeService, self).__init__(client)


    def baseURL(self):
        return 'https://feeds.api.ndustrial.io/'

    def audience(self):

        return 'CHANGEME'


    def getFeeds(self, id=None, execute=True):

        if id is None:
            uri='feeds'
        else:
            assert isinstance(id, int)
            uri='feeds/'+str(id)


        return self.execute(GET(uri=uri), execute=execute)

    def getFieldDescriptors(self, feed_id, execute=True):

        assert isinstance(feed_id, int)

        return self.execute(GET('feeds/'+str(feed_id)+'/fields'), execute=execute)

    def getUnprovisionedFields(self, feed_id, execute=True):

        assert isinstance(feed_id, int)

        return self.execute(GET('feeds/'+str(feed_id)+'/fields/unprovisioned'), execute=execute)


    def getFeedOutputs(self, feed_id, execute=True):
        assert isinstance(feed_id, int)

        return self.execute(GET('feeds/' + str(feed_id) + '/outputs'), execute=execute)

    def getUnprovisionedData(self, feed_id, field_descriptor, execute=True):
        assert isinstance(feed_id, int)
        assert isinstance(field_descriptor, str)

        return self.execute(GET('feeds/'
                                + str(feed_id)
                                + '/fields/'
                                + field_descriptor
                                +'/data'), execute=execute)

    def getData(self, output_id, field_human_name, execute=True):
        assert isinstance(output_id, int)
        assert isinstance(field_human_name, str)

        return self.execute(GET('outputs/'
                                + str(output_id)
                                + '/fields/'
                                + field_human_name
                                +'/data'), execute=execute)

    def getOutputs(self, id=None, execute=True):

        if id is None:
            uri='outputs'
        else:
            assert isinstance(id, int)
            uri='outputs/'+str(id)


        return self.execute(GET(uri=uri), execute=execute)


    def getFields(self, output_id, execute=True):

        assert isinstance(output_id, int)

        return self.execute(GET('outputs/' + str(output_id) + '/fields'), execute=execute)

