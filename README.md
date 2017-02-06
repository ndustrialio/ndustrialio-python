# ndustrialio-python
ndustrial.io Python API bindings and tools

## Authentication
In order to successfully authenticate to an API, the CLIENT_ID and CLIENT_SECRET (given by Contxt) must be available in the environment

## Prerequisites
`pip install git+https://github.com/ndustrialio/auth0-python.git`

## Example

```
from apiservices import *
from apiservices.workers import WorkerService
from apiservices.rates import RatesService

rates_service = RatesService(client_id=os.environ.get('CLIENT_ID'))

## Get rate schedules
periods = self.rates_service.getScheduleRTPPeriods(self.rate_schedule_id, orderBy='period_end', reverseOrder=True)

```


## Workers

Workers are pieces of code that interact with the ndustrial.io API.  To facilitate worker creation, there are a number
of tools in the `workertools` package.  To instantiate a worker, subclass `BaseWorker`:

```
class ExampleWorker(BaseWorker):

    def __init__(self, environment, client_id=None, client_secret=None):

        super(ExampleWorker, self).__init__(environment, client_id, client_secret)

```

Your worker must be authenticated via a client_id and secret.  If these values are not passed in, BaseWorker will attempt
to pull them from the environment variables CLIENT_ID and CLIENT_SECRET.  You must also provide your configuration
environment UUID:


| Name        | UUID           |
| ------------- |:-------------:|
| staging     | 4a9cfc2b-2580-4d01-8e67-0ea176296746 |
| production      | 64c6dde7-7830-47c1-a411-6c39c158ec79      |
| development | 84f3e772-d6b6-4ace-9c0e-36d64c62cbc6      |


`BaseWorker` will fetch any secure variables created in Contxt and place them in a dictionary at `self.config`.  Each
variable is a dictionary itself, with keys `value` and `type` for its value and type (`integer`, `string`, or `json`).
The method `getConfigurationValue` is a shortcut to accessing the `value` key of each secure variable.  To update secure
variables, call `updateConfigurationValue`.

## Test worker
You can instead subclass `TestWorker` to ease in worker development.  `TestWorker` looks for a file named `config.json`
in its root folder.  Value access is the same as `BaseWorker`, but value updating is not supported.
