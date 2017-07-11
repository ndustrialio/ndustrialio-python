import unittest
import os
from mock import patch
from ndustrialio.apiservices.feeds import FeedsService

class TestFeeds(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestFeeds, self).__init__(*args, **kwargs)
        self.client_id = os.environ.get('CLIENT_ID')
        self.client_secret = os.environ.get('CLIENT_SECRET')
        self.feeds_service = FeedsService(self.client_id, self.client_secret)

