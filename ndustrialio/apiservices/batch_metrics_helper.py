from datetime import timedelta, datetime
from scipy import stats
import numpy

def calculateNumberOfBinsAndEndTime(start_time_datetime, end_time_datetime, minute_interval):
    start_time_timedelta = timedelta(hours=start_time_datetime.hour,
                                     minutes=start_time_datetime.minute,
                                     seconds=start_time_datetime.second)
    end_time_timedelta = timedelta(hours=end_time_datetime.hour,
                                   minutes=end_time_datetime.minute,
                                   seconds=end_time_datetime.second)

    time_range_timedelta = end_time_timedelta - start_time_timedelta
    interval_timedelta = timedelta(minutes=minute_interval)

    if interval_timedelta > time_range_timedelta:
        raise Exception('Time interval should not be larger than the time range')

    num_bins = 0
    new_end_time_timedelta = start_time_timedelta

    while True:
        if (new_end_time_timedelta + interval_timedelta) > end_time_timedelta:
            break
        else:
            new_end_time_timedelta += interval_timedelta
            num_bins += 1

    new_end_time_datetime = start_time_datetime + new_end_time_timedelta

    return num_bins, new_end_time_datetime

def calculateMetrics(time_array, value_array, start_time_utc, end_time_utc, num_bins):

    metric_map = {'mean': None,
                  'minimum': None,
                  'maximum': None,
                  'standard_deviation': None,
                  'bin_edges': None}

    mean_metric_tuple = stats.binned_statistic(x=time_array,
                                               values=value_array,
                                               statistic='mean',
                                               bins=num_bins,
                                               range=(start_time_utc, end_time_utc))
    metric_map['mean'] = mean_metric_tuple[0]
    bin_edges = mean_metric_tuple[1]

    metric_map['minimum'] = stats.binned_statistic(x=time_array,
                                                   values=value_array,
                                                   statistic='min',
                                                   bins=num_bins,
                                                   range=(start_time_utc, end_time_utc))[0]

    metric_map['maximum'] = stats.binned_statistic(x=time_array,
                                                   values=value_array,
                                                   statistic='max',
                                                   bins=num_bins,
                                                   range=(start_time_utc, end_time_utc))[0]

    metric_map['standard_deviation'] = stats.binned_statistic(x=time_array,
                                                              values=value_array,
                                                              statistic=lambda y: numpy.std(y),
                                                              bins=num_bins,
                                                              range=(start_time_utc, end_time_utc))[0]

    metric_map['bin_edges'] = [datetime.fromtimestamp(bin_edge_utc) for bin_edge_utc in bin_edges]

    return metric_map
