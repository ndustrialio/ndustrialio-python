from ndustrialio.apiservices import *


class CostCentersService(Service):
    def __init__(self, client_id, client_secret=None):
        super(CostCentersService, self).__init__(client_id, client_secret)

    def baseURL(self):
        return 'https://facilities.api.ndustrial.io'

    def audience(self):
        return 'SgbCopArnGMa9PsRlCVUCVRwxocntlg0'

    def getFacilities(self, execute=True):
        return self.execute(GET(uri='facilities'), execute)

    def getFacility(self, facility_id, execute=True):
        return self.execute(GET(uri='facilities/{}'.format(facility_id)), execute)

    def getBuildingsForFacility(self, facility_id, execute=True):
        return self.execute(GET(uri='facilities/{}/buildings'.format(facility_id)), execute)

    def addFacility(self, facility_obj, execute=True):
        return self.execute(POST(uri='facilities').body(facility_obj))

    def getCostCenters(self, execute=True):
        return self.execute(GET(uri='costcenters'), execute)

    def addCostCenter(self, cost_center_obj, execute=True):
        return self.execute(POST(uri='costcenters').body(cost_center_obj))

    def addAttribute(self, attribute_obj, execute=True):
        return self.execute(POST(uri='costcenters/attributes').body(attribute_obj))

    def getAttributes(self, organization_id, execute=True):
        return self.execute(GET(uri='organizations/{}/attributes'.format(organization_id)), execute)

    def getCostCenterAttributes(self, cost_center_id, execute=True):
        return self.execute(GET(uri='costcenters/{}/attributes'.format(cost_center_id)), execute)

    def addCostCenterAttribute(self, cost_center_id, attribute_id, track_actuals, track_forecast, track_budget,
                               execute=True):
        return self.execute(POST(uri='costcenters/{}/attributes/{}'.format(cost_center_id, attribute_id)).body(
            {'track_actuals': track_actuals,
             'track_forecast': track_forecast,
             'track_budget': track_budget
             }))

    def addCostCenterActual(self, cost_center_attribute_id, actuals_obj):
        return self.execute(
            POST(uri='costcenters/attributes/{}/actuals'.format(cost_center_attribute_id)).body(actuals_obj))

    def addCostCenterBudget(self, cost_center_attribute_id, budget_obj):
        return self.execute(
            POST(uri='costcenters/attributes/{}/budgets'.format(cost_center_attribute_id)).body(budget_obj))


