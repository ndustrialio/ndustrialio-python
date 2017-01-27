import requests
import traceback
import json
from pytz import timezone as TimeZone
from ndustrialio.apiservices.ngest import NgestService
import pytz


class NgestTypeError(Exception):
    pass


class NgestClient():
    def __init__(self, feed_key, feed_token, feed_timezone):
        self.feed_key = feed_key
        self.feed_token = feed_token
        self.feed_timezone = feed_timezone
        self.ngestService = NgestService()

    def sendData(self, nGestDataObject):

        # delocalize all timestamps in the data object
        nGestDataObject.delocalizeAllTimestamps(self.feed_timezone)

        try:
            dataToSend = nGestDataObject.getJsonData()
            for dataObj in dataToSend:
                self.ngestService.sendData(self.feed_token, self.feed_key, dataObj)
        except Exception as e:
            traceback.print_exc()
            return False
        return True


class NonUniqueFieldIDException(Exception):
    pass


class NgestTimeSeriesDataObject():
    def __init__(self, feedKey):
        self.dataObj = {}
        self.dataObj['feedKey'] = feedKey
        self.dataObj['type'] = 'timeseries'
        self.dataObj['data'] = {}
        self.tsData = self.dataObj['data']

    def delocalizeAllTimestamps(self, toTimezone):
        tz = TimeZone(toTimezone)
        newDateObj = {}
        for timeObj in self.tsData:
            print ('Old time: ' + str(timeObj))
            if timeObj.tzinfo is not None:
                print ('No need to convert time...already localized')
                newDateObj[str(timeObj)] = self.tsData[timeObj]
                continue
            localDateObj = tz.localize(timeObj)
            utcDateObj = localDateObj.astimezone(pytz.utc)
            print ('New time: ' + str(utcDateObj))
            newDateObj[str(utcDateObj)] = self.tsData[timeObj]
        self.tsData = newDateObj

    def addTimeValue(self, timeObj, field_id, value):
        if timeObj not in self.tsData:
            self.tsData[timeObj] = {}
        if field_id in self.tsData[timeObj]:
            raise NonUniqueFieldIDException(
                'Field ID: %s already exists in time series at timestamp %s' % (str(field_id), str(timeObj)))
        self.tsData[timeObj][field_id] = {'value': str(value)}

    def getFeedKey(self):
        return self.dataObj['feedKey']

    def getFieldKeys(self):
        fieldKeys = []
        for ts in self.tsData:
            for key in self.tsData[ts]:
                fieldKeys.append(key)
        return fieldKeys

    def getJsonData(self):
        sortedData = []
        timestamps = sorted(self.tsData.keys())

        ### check to see how big the data is
        maxBucketLength = 50
        for timestamp in timestamps:
            print (timestamp)
            for chunk in self.dataChunks(self.tsData[timestamp].keys(), maxBucketLength):
                chunkDict = {}
                for key in chunk:
                    chunkDict[key] = self.tsData[timestamp][key]
                sortedData.append({'timestamp': timestamp,
                                   'data': chunkDict
                                   })
        exportData = []
        for data in sortedData:
            exportedDataObj = self.dataObj.copy()
            exportedDataObj['data'] = [data]
            exportData.append(json.dumps(exportedDataObj))

        return exportData

    def dataChunks(self, theList, chunkSize):
        for i in xrange(0, len(theList), chunkSize):
            yield theList[i:i + chunkSize]

    def toJson(self):
        sortedData = []

        timestamps = sorted(self.tsData.keys())

        for timestamp in timestamps:
            sortedData.append({'timestamp': timestamp,
                               'data': self.tsData[timestamp]})

        exportedDataObj = self.dataObj.copy()
        exportedDataObj['data'] = sortedData
        return json.dumps(exportedDataObj)

    def toJsonObj(self):
        sortedData = []

        timestamps = sorted(self.tsData.keys())

        for timestamp in timestamps:
            sortedData.append({'timestamp': timestamp,
                               'data': self.tsData[timestamp]})

        exportedDataObj = self.dataObj.copy()
        exportedDataObj['data'] = sortedData
        return exportedDataObj

