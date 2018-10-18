from ndustrialio.apiservices.assets import Assets
from datetime import datetime
import os

'''

Asset Type
    -> Organization
        -> Asset
            -> Attribute (key) -> Value
                Value History
            -> Metric (key)
                -> Metric Time + Value
        -> Asset Type Attributes
        -> Asset Type Metrics

Facility
    Lineage Logistics
        Assets:
            Mira Loma
                Attributes:
                    - Square Feet: 126,000
                    - Cubic Feet: 1,300,000
                    - Rate Schedule ID: 87762
                    - Utility Tracked: True
                Metrics:
                    - Utility Spend (Monthly):
                        - May 1 -> May 31 2018: $12,365
                        - June 1 -> June 30 2018: $15,678
                    - Utility Spend (Annually):
                        - Jan 1 -> Dec 31 2017: $167,890
                        - Jan 1 -> Dec 31 2018: *
            Geneva
                Attributes:
                    - Square Feet: 129,000
                    - Cubic Feet: *
                    - Rate Schedule ID: 87762
                    - Utility Tracked: False
                Metrics:
                    - Utility Spend (Monthly):
                        - *
                    - Utility Spend (Annually):
                        - *        

        Attributes:
            Square Feet
            Cubic Feet
            Rate Schedule ID
            Utilities Tracked

        Metrics:
            Utility Spend (Monthly)
            Utility Spend (Annually)

Org-Level
- Get all asset types for an organization
- Get all assets for a given type
- Create a new asset for a type

Asset Values (for a given asset type)
- Get all attribute values for a single asset in a map
- Get all values of a single attribute for all assets
- Get all metrics available for a asset
- Get all values of a single metric for a certain time for all assets


'''

wp_assets = Assets('a8e526e4-cb2d-4188-ac25-294e76f9f467', os.environ.get('CLIENT_ID'))

facilities = wp_assets.Facility.getAll()

#new_asset = lineage_assets.Facility.create(label='Mira Loma', description='My bomb ass facility')\
#                .withAttributes(zip_code=28625, square_feet=126000)

print(facilities)
'''
print(new_asset)
print(new_asset.zip_code(1234, effective_date=datetime.now()))
print(new_asset)
new_asset.zip_code.set(9876, effective_date=datetime.now())
print(new_asset)
print(new_asset.zip_code())
'''

# can we really do this? you've an asset type id and a label of an asset, but there's no
# restriction saying a label must be unique for a asset type. There could be a bunch of
# these (Building 1 for example). What we could do is add a filter saying, "I want
# Building 1 from this Facility (assuming we have a relationship defined in the future)"
oxnard = lineage_assets.Facility.get('Oxnard').first() # this could return more than 1 record...





'''
oxnard.loadAssets()
oxnard_feeds = oxnard.IOT.Feeds.getAll()

oxnard_rate_schedule = oxnard.Rates.getSchedule()

oxnard.Utilities.Accounts.getAll()
oxnard_meters = oxnard.Utilities.Meters.getAll()

for meter in oxnard_meters:
    statements = meter.Statements.getAll()
    for statement in statements:
        print(statement)


#(come back to this...does this make sense to do?) facilities.zip_code.all()
lineage_assets.Facility.create(label='Mira Loma')
facilities.add(label='Mira Loma').withAttributes([])
lineage_assets.getAssetById('<some_asset_id>')

for facility in facilities:
    print(facility)

    facility.zip_code.update(28625)
    facility.zip_code

    for attribute in facility.getCurrentAttributes():
        print(attribute)
        ''
            Square Feet: 126,000
            Cubic Feet: 1,300,000
            Rate Schedule ID: 87762
            Utility Tracked: True
        ''
    spend = facility.utility_spend(from_date=datetime(year=2018, month=1, day=1))
    for value in spend:
        print(value)

    for metric in facility.getAvailableMetrics():
        print(metric)
        ''
        Utility Spend(Monthly)
        Utility Spend(Annually)
        ''

        metric.addValue(from_date=datetime(year=2018, month=1, day=1), to_date=datetime.now(), value=12345)

        for value in facility.getValuesForMetric(metric):
            print(value)
            ''
            - May 1 -> May 31 2018: $12,365
            - June 1 -> June 30 2018: $15,678
            ''
'''