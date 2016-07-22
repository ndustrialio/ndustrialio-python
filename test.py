from apiservices import ServiceInitializer
from apiservices.opsmetric import OpsmetricService
import os

initializer = ServiceInitializer(access_token=os.environ.get('ACCESS_TOKEN'))

opsmetric_service = initializer.init_service(OpsmetricService)

translations = opsmetric_service.getTranslations(1,1)

print str(translations)