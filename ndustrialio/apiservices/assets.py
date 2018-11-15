import json
import inflect
from ndustrialio.apiservices import *

p = inflect.engine()


class InvalidAttributeException(Exception):
    pass


class AssetConfigurationException(Exception):
    pass


class InvalidAssetException(Exception):
    pass


class AssetMetric:

    def __init__(self, asset_type_obj, api_object):
        self.asset_type = asset_type_obj
        for key, value in api_object.items():
            setattr(self, key, value)

        self.is_global = True if self.organization_id is None else False


class AssetAttribute:

    def __init__(self, asset_type_obj, api_object):
        self.asset_type = asset_type_obj
        for key, value in api_object.items():
            setattr(self, key, value)

        self.is_global = True if self.organization_id is None else False


class AssetAttributeValue:

    def __init__(self, assets_instance, asset_obj, asset_attribute_obj, api_object):
        self.assets_instance = assets_instance
        self.asset_obj = asset_obj
        self.asset_attribute_obj = asset_attribute_obj
        for key, value in api_object.items():
            if not isinstance(value, dict):
                setattr(self, key, value)
            if key == 'asset_attribute':
                for attribute_key, attribute_value in value.items():
                    setattr(self,  attribute_key, attribute_value)

    '''
        Update the value of an asset attribute value
    '''
    def set(self, value, effective_date=None):
        print('Setting new value for Attribute {} of Asset {} as {} with effective_date {}'
              .format(self.asset_attribute_obj.label, self.asset_obj.label, value, effective_date))

        body = {
            'value': value,
            'effective_date': effective_date if not None else str(datetime.today())
        }

        self.assets_instance.update_attribute_value(asset_attribute_value_obj=self, api_body=body)

        # update the values in this instance
        self.value = value
        self.effective_date = body['effective_date']

        return self

    def __str__(self):
        return str('{} -> {}'.format(self.label, self.value))

    def __repr__(self):
        return str('{} -> {}'.format(self.label, self.value))

    def __call__(self, value=None, effective_date=None):

        if value is not None:
            self.set(value, effective_date)

        return self


class Asset:

    def __init__(self, assets_instance, asset_type_obj, api_object):
        self.assets_instance = assets_instance
        self.asset_type = asset_type_obj
        for key, value in api_object.items():
            setattr(self, key, value)

        self.attribute_values = {}

    def withAttributes(self, **kwargs):
        print('Creating with attributes')
        print(kwargs)
        for key, value in kwargs.items():
            if key not in self.asset_type.attributes:
                raise InvalidAttributeException("Attribute {} does not exist for type {}".format(key, self.asset_type.label))
            body = {'value': value,
                    'effective_date': str(datetime(year=2018, month=1, day=1)) ## set this for now until FM-200 is fixed
                    }
            # returns an AssetAttributeValue object
            self.attribute_values[key] = self.assets_instance.create_attribute_value(asset_obj=self,
                                                                                     asset_attribute_obj=self.asset_type.attributes[key],
                                                                                     api_body=body)
            setattr(self, key, value)
            setattr(self, key, self.attribute_values[key].value)

        return self

    def attributes(self, force_fetch=False):
        if force_fetch or len(self.attribute_values) == 0:
            print('Getting all attributes for asset {}'.format(self.label))
            attribute_values = self.assets_instance.get_attribute_values_for_asset(self, asset_type_obj=self.asset_type)
            # store as a map to self
            for item in attribute_values:
                self.attribute_values[item.label] = item
                setattr(self, item.label, item.value)

            # Set None for attributes not populated
            for key in self.asset_type.attributes:
                if key not in self.attribute_values:
                    setattr(self, key, None)
        return self.attribute_values

    def __str__(self):
        return "<Asset: asset_id: '{}', label: '{}', description: '{}', attributes: {}>".format(
            self.id, self.label, self.description, self.attribute_values)

    def __repr__(self):
        return "<Asset: asset_id: '{}', label: '{}', description: '{}', attributes: {}>".format(
            self.id, self.label, self.description, self.attribute_values)

    def toJSON(self):
        print(self.__dict__)
        return self.__dict__

class AssetList:

    def __init__(self, asset_type_obj):
        pass


class AssetType:

    valid_asset_create_fields = ['label', 'description']

    def __init__(self, assets_instance, organization_id, type_obj):
        self.id = type_obj['id']
        self.organization_id = organization_id
        self.label = type_obj['label']
        self.label_plural = p.plural(self.label)
        self.description = type_obj['description']
        self.is_global = True if self.organization_id is None else False
        self.assets_instance = assets_instance
        self.attributes = {}
        self.metrics = {}
        self.assets = []

        '''
        # Set attributes
        self.attributes = {}
        for key, value in config['attributes'].items():
            self.attributes[key] = AssetAttribute(id=value['id'], asset_type_obj=self, type=value['type'], label=key,
                                                  description=None, is_required=False)
        '''

    def set_attributes(self, attribute_objs):
        for attribute in attribute_objs:
            self.attributes[attribute.label] = attribute

    def set_metrics(self, metric_objs):
        for metric in metric_objs:
            self.metrics[metric.label] = metric

    def create(self, label, description=None):
        asset_obj = self.assets_instance.create_asset(asset_type_obj=self, api_body={
            'label': label,
            'description': description,
            'asset_type_id': self.id,
            'organization_id': self.assets_instance.organization_id
        })
        self.assets.append(asset_obj)
        return asset_obj

    def getAll(self, force_fetch=False):
        if force_fetch or len(self.assets) == 0:
            print('Getting all {} for organization_id {}'.format(self.label_plural, self.organization_id))
            self.assets = self.assets_instance.get_assets_for_type(self)
        return self.assets

    # TODO cleanup
    def toJSON(self):
        obj = []
        if len(self.assets) == 0:
            self.getAll()

        for asset in self.assets:
            obj.append(asset.toJSON())


    # TODO - implement me
    def get(self, asset_label):
        print('Getting asset with type {} and label {}'.format(self.label, asset_label))

    def __str__(self):
        return "<AssetType: asset_type_id: '{}', label: '{}', description: '{}', attributes: {}>".format(
            self.id, self.label, self.description, self.attributes.keys())

    def __call__(self):
        return self


class Assets(Service):

    def __init__(self, organization_id, client_id):

        super(Assets, self).__init__(client_id=client_id)
        self.organization_id = organization_id
        self.load_configuration()
        self.types_by_id = {}

        '''
        self.asset_config = self.load_org_asset_configuration()
        
        for type_label, type_config in self.asset_config[self.organization_id]['AssetTypes'].items():
            print(type_label)
            type_class_obj = AssetType(organization_id, type_label, type_config)
            setattr(self, type_label, type_class_obj)
            setattr(self, type_label.capitalize(), type_class_obj)
        '''

    def baseURL(self):
        return 'https://facilities.api.ndustrial.io'

    def audience(self):
        return 'SgbCopArnGMa9PsRlCVUCVRwxocntlg0'

    def load_configuration(self):
        print('Loading Asset Configuration for Organization')
        asset_types = PagedResponse(self.execute(GET(uri='assets/types'), execute=True))
        for asset_type in asset_types:
            self._load_configuration_for_type(asset_type)

    def _load_configuration_for_type(self, asset_type_obj):
        type_class_obj = AssetType(assets_instance=self,
                                   organization_id=self.organization_id,
                                   type_obj=asset_type_obj)
        setattr(self, type_class_obj.label.replace(' ', ''), type_class_obj)
        setattr(self, type_class_obj.label.capitalize().replace(' ', ''), type_class_obj)

        type_class_obj.set_attributes(self.get_attributes_for_type(type_class_obj))
        type_class_obj.set_metrics(self.get_metrics_for_type(type_class_obj))

    def get_attributes_for_type(self, asset_type_obj):
        attributes = PagedResponse(self.execute(GET(uri='assets/types/{}/attributes'.format(asset_type_obj.id)), execute=True))
        return [AssetAttribute(asset_type_obj=asset_type_obj, api_object=record) for record in attributes]

    def get_metrics_for_type(self, asset_type_obj):
        metrics = PagedResponse(self.execute(GET(uri='assets/types/{}/metrics'.format(asset_type_obj.id)), execute=True))
        return [AssetMetric(asset_type_obj=asset_type_obj, api_object=record) for record in metrics]

    def get_assets_for_type(self, asset_type_obj):
        parameters = {
            'asset_type_id': asset_type_obj.id
        }
        assets = PagedResponse(self.execute(
            GET(uri='organizations/{}/assets'.format(self.organization_id)).params(parameters),
            execute=True))
        return [Asset(assets_instance=self, asset_type_obj=asset_type_obj, api_object=record) for record in assets]

    def get_attribute_values_for_asset(self, asset_obj, asset_type_obj):
        values = self.execute(GET(uri='assets/{}/attributes/values'.format(asset_obj.id)), execute=True)
        attribute_value_objects = []
        for record in values:
            attribute_obj = asset_type_obj.attributes[record['asset_attribute']['label']]
            attribute_value_objects.append(AssetAttributeValue(assets_instance=self,
                                                               asset_obj=asset_obj,
                                                               asset_attribute_obj=attribute_obj,
                                                               api_object=record)
                                           )
        return attribute_value_objects

    def create_asset(self, asset_type_obj, api_body):
        asset_response = self.execute(POST(uri='/assets').body(api_body), execute=True)
        return Asset(assets_instance=self, asset_type_obj=asset_type_obj, api_object=asset_response)

    def create_attribute_value(self, asset_obj, asset_attribute_obj, api_body):
        # /assets/:asset_id/attributes/:asset_attribute_id/values
        api_body['asset_attribute_id'] = asset_attribute_obj.id
        attribute_value_response = self.execute(
            POST(uri='/assets/{}/attributes/{}/values'.format(asset_obj.id, asset_attribute_obj.id)).body(api_body),
            execute=True)
        return AssetAttributeValue(assets_instance=self,
                                   asset_obj=asset_obj,
                                   asset_attribute_obj=asset_attribute_obj,
                                   api_object=attribute_value_response)

    def update_attribute_value(self, asset_attribute_value_obj, api_body):
        # /assets/attributes/values/:asset_attribute_value_id
        self.execute(
            PUT(uri='/assets/attributes/values/{}'.format(asset_attribute_value_obj.id)).body(api_body),
            execute=True)
        return True

    def load_org_asset_configuration(self):
        with open('./ndustrialio/apiservices/asset_fixture.json') as config_file:
            asset_config = json.load(config_file)

        asset_config_by_org = {}
        for organization_config in asset_config:
            asset_config_by_org[organization_config['organization_id']] = organization_config

        if self.organization_id not in asset_config_by_org:
            raise AssetConfigurationException('Error! Organization ID not in asset configuration')

        return asset_config_by_org

    def _get_all_assets(self):
        parameters = { 'organization_id': self.organization_id}
        assets = PagedResponse(self.execute(GET(uri='assets').params(parameters), execute=True))
        return [Asset]

    def hasType(self, type_name):
        return hasattr(self, type_name)

    def newType(self, type_name, description):
        type = AssetType(assets_instance=self, organization_id=self.organization_id,)




