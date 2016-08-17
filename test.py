from apiservices import ServiceInitializer, BatchService
from apiservices.opsmetric import OpsmetricService
from apiservices.facilities import FacilityService
from apiservices.workers import WorkerService
import os

initializer = ServiceInitializer(access_token=os.environ.get('ACCESS_TOKEN'))

opsmetric_service = initializer.init_service(OpsmetricService)
batch_service = initializer.init_service(BatchService)
facility_service = initializer.init_service(FacilityService)
worker_service = initializer.init_service(WorkerService)


#translations = opsmetric_service.getTranslations(1,1)

#print str(translations)


#batch_response = batch_service.batchRequest(requests={'request1': opsmetric_service.getTranslations(1,1, execute=False),
#                                     'request2': opsmetric_service.getSystems(execute=False)})

#print (str(batch_response))


worker_configs = worker_service.getConfigurationValues(id='a3771b1d-8378-e6ea-aecf-6d0ca43c047e', environment='production', execute=True)

print(str(worker_configs))