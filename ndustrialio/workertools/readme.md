# nGest

nGest is a simple JSON format for pushing data to the ndustrial.io data ingestion system.  

## Message format
```
{
    "data": [
        {
            "timestamp": "2018-02-27 14:42:53",
            "data": {
                "example_field": {
                    "value": "32"
                }
            }
        },
        {
            "timestamp": "2018-02-27 14:35:53",
            "data": {
                "example_field": {
                    "value": "25"
                }
            }
        },
        {
            "timestamp": "2018-02-27 14:29:53",
            "data": {
                "example_field": {
                    "value": "19"
                }
            }
        },
        {
            "timestamp": "2018-02-27 14:12:53",
            "data": {
                "example_field": {
                    "value": "2"
                }
            }
        },
        {
            "timestamp": "2018-02-27 14:37:53",
            "data": {
                "example_field": {
                    "value": "27"
                }
            }
        },
        {
            "timestamp": "2018-02-27 14:51:53",
            "data": {
                "example_field": {
                    "value": "41"
                }
            }
        },
        {
            "timestamp": "2018-02-27 14:16:53",
            "data": {
                "example_field": {
                    "value": "6"
                }
            }
        },
        {
            "timestamp": "2018-02-27 14:17:53",
            "data": {
                "example_field": {
                    "value": "7"
                }
            }
        },
        {
            "timestamp": "2018-02-27 14:23:53",
            "data": {
                "example_field": {
                    "value": "13"
                }
            }
        },
        {
            "timestamp": "2018-02-27 14:57:53",
            "data": {
                "example_field": {
                    "value": "47"
                }
            }
        }
    ],
    "type": "timeseries",
    "feedKey": "example_feed"
}
```

Within an individual timestamp, only unique fields are allowed.  The reference implementation allows only 50 indivdual data points (50 timestamps of 1 field, or 1 timestamp with 50 different fields) per message. Currently the only supported value of the `type` key is `timeseries`. 

## Push URL format

`https://data.ndustrial.io/v1/<feed_token>/ngest/<feed_key>`


## Tokens and Keys
A feed token is issued by ndustrial.io and authorizes a feed to push data.  It is provided when a feed is registered.  A feed key is a string that identifies the data stream in the ndustrial.io backend.  
