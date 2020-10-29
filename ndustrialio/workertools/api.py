import os, sys
from datetime import datetime
import datetime as DT
import boto
from boto.s3.connection import S3Connection
from boto.s3.bucket import Bucket
from boto.s3.key import Key
from psycopg2 import IntegrityError

boto.config.add_section('Boto')
boto.config.set('Boto', 'http_socket_timeout', '10')

class APIFileSaver():
    def __init__(self, apiDBConnection, accessKeyID=None, secretAccessKey=None):
        self.s3 = None
        self.psql = apiDBConnection
        self.systemUserID = 18
        self.accessKeyID = accessKeyID
        self.secretAccessKey = secretAccessKey

    def initS3(self):
        if self.accessKeyID:
            self.s3 = S3Connection(self.accessKeyID, self.secretAccessKey)
        else:
            self.s3 = S3Connection(os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'])
        self.s3bucket = self.s3.get_bucket('sis-api-production')

    def saveFile(self, fileName, file_category_id, local_filepath, description='', facility_id=None,
                 organization_id=None, content_type='', superuser_required=False):
        apiFile = APIBackedFile()
        if self.s3 is None:
            self.initS3()
        return apiFile.save(self.s3, self.s3bucket, self.psql, self.systemUserID, fileName, file_category_id,
                            local_filepath, description, facility_id, organization_id, content_type, superuser_required)


class S3ConnectionException(Exception):
    pass


class APIBackedFile():
    def __init__(self):
        pass

    def save(self, s3Connection, s3bucket, psqlConnection, created_by, fileName, file_category_id, local_filepath,
             description='', facility_id=None, organization_id=None, content_type='', superuser_required=False):
        if s3Connection is None:
            raise S3ConnectionException('S3 Connection not initialized!')
        k = Key(s3bucket)
        k.key = fileName
        base_filename = os.path.basename(fileName)
        print (k.key)
        print ('Uploading local file: ' + str(local_filepath))
        k.set_contents_from_filename(local_filepath, cb=self.trackProgress, num_cb=20)
        return_id = None
        try:
            query = "select * from files where filename ='%s' order by version DESC limit 1" % (k.key)
            existing_files = psqlConnection.complicatedSelectExecution(query, dictResults=True)
            if len(existing_files) > 0:
                version = int(existing_files[0]['version']) + 1
            else:
                version = 1

            return_id = psqlConnection.insertOne("files", {'filename': k.key,
                                                           'base_filename': base_filename,
                                                           'description': description,
                                                           'content_type': content_type,
                                                           'status': "ACTIVE",
                                                           'superuser_required': superuser_required,
                                                           'version': version,
                                                           'file_category_id': file_category_id,
                                                           'created_by': created_by,
                                                           'updated_at': datetime.now()
                                                           })
            if facility_id is not None:
                psqlConnection.insertOne("facility_files", {'facility_id': facility_id,
                                                            'file_id': return_id
                                                            }, returning="facility_id")
            if organization_id is not None:
                psqlConnection.insertOne("organization_files", {'organization_id': organization_id,
                                                                'file_id': return_id
                                                                })
        except IntegrityError as ie:
            print ('ERROR: File already exists! Skipping')
            return_id = None

        return return_id

    def trackProgress(self, complete, total):
        sys.stdout.write('.')
        sys.stdout.flush()
        if complete == total:
            print ('')


class RateScheduleCalculationException(Exception):
    pass


class APIRateSchedule():
    def __init__(self, psql, schedule_id):
        self.psql = psql
        self.schedule_id = schedule_id
        self.schedule = []

    def getUsageRateSchedule(self):
        query = 'select * from energy_seasons inner join energy_season_periods esp on esp.energy_season_id=energy_seasons.id inner join energy_tier_rates etr on etr.energy_season_period_id=esp.id  where rate_schedule_id=%s' % (
            self.schedule_id)
        rows = self.psql.complicatedSelectExecution(query, dictResults=True)
        for row in rows:
            self.schedule.append(row)

    def getDemandRateSchedule(self):
        query = 'select * from demand_seasons inner join demand_season_periods dsp on dsp.demand_season_id=demand_seasons.id inner join demand_tier_rates dtr on dtr.demand_season_period_id=dsp.id where rate_schedule_id=%s' % (
            self.schedule_id)
        rows = self.psql.complicatedSelectExecution(query, dictResults=True)
        for row in rows:
            self.schedule.append(row)

    def rateTiersForDateAndValue(self, date, tierRateValue):
        month = date.month
        day = date.day
        weekday = date.weekday()
        hour = date.hour

        matchedSchedule = None
        for schedule in self.schedule:
            if not (month <= schedule['end_month'] and month >= schedule['start_month']):
                continue
            if not (day <= schedule['end_day'] and day >= schedule['start_day']):
                continue
            if not (weekday <= schedule['day_of_week_end'] and weekday >= schedule['day_of_week_start']):
                continue
            if not (hour < schedule['hour_end'] and hour >= schedule['hour_start']):
                continue
            if not (tierRateValue <= schedule['unit_stop_value'] and tierRateValue >= schedule['unit_start_value']):
                continue

            if matchedSchedule is not None:
                raise RateScheduleCalculationException('More that one matched schedule!')
            matchedSchedule = schedule

            if matchedSchedule is None:
                raise RateScheduleCalculationException('No matched schedule!')
        return matchedSchedule

    def rateTiersForDate(self, date):
        month = date.month
        day = date.day
        weekday = date.weekday()
        hour = date.hour

        matchedScheduleWithTiers = []
        for schedule in self.schedule:
            scheduleStartDate = DT.date(date.year, schedule['start_month'], schedule['start_day'])
            scheduleEndDate = DT.date(date.year, schedule['end_month'], schedule['end_day'])
            if not (scheduleStartDate <= date <= scheduleEndDate):
                continue
            if not (weekday <= schedule['day_of_week_end'] and weekday >= schedule['day_of_week_start']):
                continue
            if not (hour < schedule['hour_end'] and hour >= schedule['hour_start']):
                continue

            matchedScheduleWithTiers.append(schedule)

        if len(matchedScheduleWithTiers) == 0:
            raise RateScheduleCalculationException('No matched schedules!')
        return matchedScheduleWithTiers

    def ratesForSingleDay(self, date, usageValue):
        month = date.month
        day = date.day
        weekday = date.weekday()

        matchedSchedules = []
        for schedule in self.schedule:
            scheduleStartDate = DT.date(date.year, schedule['start_month'], schedule['start_day'])
            scheduleEndDate = DT.date(date.year, schedule['end_month'], schedule['end_day'])
            if not (scheduleStartDate <= date <= scheduleEndDate):
                continue
            if not (schedule['day_of_week_end'] >= weekday >= schedule['day_of_week_start']):
                continue
            if not (schedule['unit_stop_value'] >= int(usageValue) >= schedule['unit_start_value']):
                continue

            matchedSchedules.append(schedule)
        if len(matchedSchedules) == 0:
            raise RateScheduleCalculationException('No matched schedules!')
        return matchedSchedules
