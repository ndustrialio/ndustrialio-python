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

    def __init__(self, asset_attribute_obj, asset, value, effective_date=None, notes=None):
        self.asset_attribute = asset_attribute_obj
        self.asset = asset
        self.effective_date = effective_date
        self.value = value
        self.notes = notes

    '''
        Update the value of an asset attribute value
    '''
    def set(self, value, effective_date=None):
        # TODO -- persist value
        print('Setting new value for Attribute {} of Asset {} as {} with effective_date {}'
              .format(self.asset_attribute.id, self.asset.label, value, effective_date))

        self.value = value
        self.effective_date = effective_date
        return self

    def persist(self):
        # POST to /assets/:asset_id/attributes/:asset_attribute_id/values
        body = {
            'value': self.value,
            'effective_date': self.effective_date,
            'notes': self.notes
        }
        print('Creating attribute value with body:')
        print(body)

        return self

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    def __call__(self, value=None, effective_date=None):

        if value is not None:
            self.set(value, effective_date)

        return self


class Asset:

    def __init__(self, asset_type_obj, api_object):
        self.asset_type = asset_type_obj
        for key, value in api_object.items():
            setattr(self, key, value)

        self.attribute_values = {}

    '''
    Needed fields:
        asset_type_id: uuid,
        label: string
        description: string
        organization_id: string
    '''
    def create(self):
        # POST to /assets
        print('Creating {} asset with: '.format(self.label))
        body = {
            'label': self.label,
            'description': self.description,
            'asset_type_id': self.asset_type.id,
            'organization_id': self.asset_type.organization_id
        }
        print(body)

        return self

    def withAttributes(self, **kwargs):
        print('Creating with attributes')
        print(kwargs)
        for key, value in kwargs.items():
            if key not in self.asset_type.attributes:
                raise InvalidAttributeException("Attribute {} does not exist for type {}".format(key, self.asset_type.label))
            self.attribute_values[key] = AssetAttributeValue(self.asset_type.attributes[key], self, value)
            self.attribute_values[key].persist()
            setattr(self, key, value)
            setattr(self, key, self.attribute_values[key])

        return self

    def __str__(self):
        return "<Asset: asset_id: '{}', label: '{}', description: '{}', attributes: {}>".format(
            self.id, self.label, self.description, self.attribute_values)

    def __repr__(self):
        return "<Asset: asset_id: '{}', label: '{}', description: '{}', attributes: {}>".format(
            self.id, self.label, self.description, self.attribute_values)


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
        asset_obj = Asset(self, label, description)
        return asset_obj.create()

    def getAll(self, force_fetch=False):
        if force_fetch or len(self.assets) == 0:
            print('Getting all {} for organization_id {}'.format(self.label_plural, self.organization_id))
            self.assets = self.assets_instance.get_assets_for_type(self)
        return self.assets

    def get(self, asset_label):
        print('Getting asset with type {} and label {}'.format(self.label, asset_label))


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
        asset_types = PagedResponse(self.execute(GET(uri='assets/types'), execute=True))
        for asset_type in asset_types:
            self._load_configuration_for_type(asset_type)

    def _load_configuration_for_type(self, asset_type_obj):
        print(asset_type_obj['label'])
        type_class_obj = AssetType(assets_instance=self,
                                   organization_id=self.organization_id,
                                   type_obj=asset_type_obj)
        setattr(self, type_class_obj.label, type_class_obj)
        setattr(self, type_class_obj.label.capitalize(), type_class_obj)

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
        assets = PagedResponse(self.execute(GET(uri='organizations/{}/assets'.format(self.organization_id)).params(parameters), execute=True))
        return [Asset(asset_type_obj=asset_type_obj, api_object=record) for record in assets]

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




