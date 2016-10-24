from apiservices import *
from apiservices.workers import WorkerService
from apiservices.rates import RatesService




worker_service = WorkerService()

rates_service = RatesService(client_id='Y7OOKIEDvsb7t1UiF9BMGg3R1WdYgNFi')

schedules = rates_service.getSchedules()

workers = worker_service.get()


print schedules


print workers