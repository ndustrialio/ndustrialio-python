# nGest

nGest is a simple JSON format for pushing data to the ndustrial.io data ingestion system.  

## Message format
```
{
    "data": [
        {
            "timestamp": "2017-01-27 08:08:00",
            "data": {
                "example_field": "28.0"
            }
        },
        {
            "timestamp": "2017-01-27 08:05:00",
            "data": {
                "example_field": "27.7",
                "example_field3": "27.7",
                "example_field2": "27.7",
                "example_field6": "27.7",
                "example_field5": "27.7",
                "example_field4": "27.7"
            }
        },
        {
            "timestamp": "2017-01-27 08:07:00",
            "data": {
                "example_field": "27.9"
            }
        },
        {
            "timestamp": "2017-01-27 08:04:00",
            "data": {
                "example_field": "27.6"
            }
        },
        {
            "timestamp": "2017-01-27 08:03:00",
            "data": {
                "example_field3": "27.5",
                "example_field2": "27.5",
                "example_field": "27.5",
                "example_field5": "27.5",
                "example_field4": "27.5"
            }
        },
        {
            "timestamp": "2017-01-27 08:06:00",
            "data": {
                "example_field": "27.8"
            }
        }
    ],
    "type": "timeseries",
    "feedKey": "example"
}
```

Within an individual timestamp, only unique fields are allowed.  The reference implementation allows only 50 indivdual data points (50 timestamps of 1 field, or 1 timestamp with 50 different fields) per message. Currently the only supported value of the `type` key is `timeseries`. 

## Push URL format

`https://data.ndustrial.io/v1/<feed_token>/ngest/<feed_key>`


## Tokens and Keys
A feed token is issued by ndustrial.io and authorizes a feed to push data.  It is provided when a feed is registered.  A feed key is a string that identifies the data stream in the ndustrial.io backend.  
