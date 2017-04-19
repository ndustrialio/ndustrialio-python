from datetime import timedelta, datetime
from scipy import stats


class DataHelper:

    def __init__(self):
        pass

    def calculateNumberOfBinsAndEndTime(self, start_time_datetime, end_time_datetime, minute_interval):

        time_range_minutes = divmod((end_time_datetime - start_time_datetime).total_seconds(), 60)[0]
        interval_timedelta = timedelta(minutes=minute_interval)

        if minute_interval > time_range_minutes:
            raise Exception('Time interval should not be larger than the time range')

        num_bins = 0
        new_end_time_datetime = start_time_datetime

        while True:
            if (new_end_time_datetime + interval_timedelta) > end_time_datetime:
                break
            else:
                new_end_time_datetime += interval_timedelta
                num_bins += 1

        return num_bins, new_end_time_datetime

    def calculateMetrics(self, time_array, value_array, start_time_utc, end_time_utc, num_bins):

        metric_map = {'mean': None,
                      'minimum': None,
                      'maximum': None,
                      'standard_deviation': None,
                      'bin_edges': None}

        mean_metric_tuple = stats.binned_statistic(x=time_array,
                                                   values=value_array,
                                                   statistic='mean',
                                                   bins=num_bins,
                                                   range=[(start_time_utc, end_time_utc)])
        metric_map['mean'] = mean_metric_tuple[0]
        bin_edges = mean_metric_tuple[1]

        metric_map['minimum'] = stats.binned_statistic(x=time_array,
                                                       values=value_array,
                                                       statistic='min',
                                                       bins=num_bins,
                                                       range=[(start_time_utc, end_time_utc)])[0]

        metric_map['maximum'] = stats.binned_statistic(x=time_array,
                                                       values=value_array,
                                                       statistic='max',
                                                       bins=num_bins,
                                                       range=[(start_time_utc, end_time_utc)])[0]

        metric_map['standard_deviation'] = stats.binned_statistic(x=time_array,
                                                                  values=value_array,
                                                                  statistic='std',
                                                                  bins=num_bins,
                                                                  range=[(start_time_utc, end_time_utc)])[0]

        metric_map['bin_edges'] = [datetime.fromtimestamp(bin_edge_utc) for bin_edge_utc in bin_edges]

        return metric_map
