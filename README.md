# ndustrialio-python
ndustrial.io Python API bindings and tools

## Authentication
In order to successfully authenticate to an API, the CLIENT_ID and CLIENT_SECRET (given by Contxt) must be available in the environment

## Example

```
from apiservices import *
from apiservices.workers import WorkerService
from apiservices.rates import RatesService

rates_service = RatesService(client_id=os.environ.get('CLIENT_ID'))

## Get rate schedules
periods = self.rates_service.getScheduleRTPPeriods(self.rate_schedule_id, orderBy='period_end', reverseOrder=True)

```
