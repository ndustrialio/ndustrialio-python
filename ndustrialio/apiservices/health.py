from enum import Enum
from datetime import datetime
from pytz import UTC

from ndustrialio.apiservices import Service, POST


class HealthStatus(Enum):
    GOOD = 'healthy'
    BAD = 'unhealthy'


class HealthService(Service):

    def __init__(self, client_id, client_secret=None):
        super(HealthService, self).__init__(client_id, client_secret)

    def baseURL(self):
        return 'https://health.api.ndustrial.io/v1'

    def audience(self):
        return '6uaQIV1KnnWhXiTm09iGDvy2aQaz2xVI'

    def report(self, org_id, asset_id, status=HealthStatus.GOOD, timestamp=datetime.now(tz=UTC).isoformat(), execute=True):
        body = {
            status: status,
            timestamp: timestamp
        }

        return self.execute(POST(uri='{}/assets/{}'.format(org_id, asset_id))
                            .body(body))
