import slackclient



class SlackUtility:

    def __init__(self, token):

        self.client = slackclient.SlackClient(token=token)


    def sendMessage(self, message, channel, botname):

        self.client.api_call('chat.postMessage', text=message, channel=channel, username=botname)
