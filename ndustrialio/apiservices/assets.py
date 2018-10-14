import json
import inflect

p = inflect.engine()


class AssetConfigurationException(Exception):
    pass


class InvalidAssetException(Exception):
    pass


class AssetAttribute():

    def __init__(self):
        pass


class Asset():

    def __init__(self, asset_type_obj, label, description):
        self.asset_type = asset_type_obj
        self.label = label
        self.description = description
        self.id = 'no_asset_id'  # TO-DO add to constructor

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


class AssetList():

    def __init__(self, asset_type_obj):
        pass


class AssetType():

    valid_asset_create_fields = ['label', 'description']

    def __init__(self, organization_id, label, config):
        self.id = 'no_id'
        self.organization_id = organization_id
        self.label = label
        self.label_plural = p.plural(self.label)
        self.config = config
        self.attributes = config['attributes']
        self.is_global = config['is_global']
        self.metrics = config['metrics']

    def create(self, label, description=None):
        asset_obj = Asset(self, label, description)
        return asset_obj.create()

    def getAll(self):
        print('Getting all {} for organization_id {}'.format(self.label_plural, self.organization_id))

    def get(self, asset_label):
        print('Getting asset with type {} and label {}'.format(self.label, asset_label))


class Assets(object):

    def __init__(self, organization_id):
        self.organization_id = organization_id
        self.asset_config = self.load_org_asset_configuration()

        for type_label, type_config in self.asset_config[self.organization_id]['AssetTypes'].items():
            print(type_label)
            type_class_obj = AssetType(organization_id, type_label, type_config)
            setattr(self, type_label, type_class_obj)
            setattr(self, type_label.capitalize(), type_class_obj)


    def load_org_asset_configuration(self):
        with open('./ndustrialio/apiservices/asset_fixture.json') as config_file:
            asset_config = json.load(config_file)

        asset_config_by_org = {}
        for organization_config in asset_config:
            asset_config_by_org[organization_config['organization_id']] = organization_config

        if self.organization_id not in asset_config_by_org:
            raise AssetConfigurationException('Error! Organization ID not in asset configuration')

        return asset_config_by_org



