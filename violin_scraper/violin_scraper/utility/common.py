from scrapy import shell

import os
import datetime
import re


def inspect(response, spider):
    if spider.debug_mode:
        spider.logger.debug('========> Start inspecting')
        shell.inspect_response(response, spider)
        spider.logger.debug('<======== Finish inspecting')


def running_path():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def str_to_datetime(str):
    """
    input:
    '2020-06-27 22:03:20.642914'
    """
    pattern = r'-|:|\.| +'
    array = re.split(pattern, str)
    str_array = [int(n) for n in array]

    return datetime.datetime(*str_array)


def str_to_datetime_(str):
    """
    Obsoleted, it is too complex and inflexible.
    """
    year_str, month_str, day_str, hour_str, minute_str, second_str, ms_str = '0', '0', '0', '0', '0', '0', '0'

    date_time_array = str.split(' ')
    if len(date_time_array) == 0:
        raise Exception('An unrecognized date format')
    elif len(date_time_array) == 1:
        date_str = date_time_array[0]
    else:
        date_str = date_time_array[0]
        time_str = date_time_array[1]
        hour_str, minute_str, second_str = time_str.split('.')[0].split(':')
        ms_str = time_str.split('.')[1]

    year_str, month_str, day_str = date_str.split('-')
    return datetime.datetime(int(year_str), int(month_str), int(day_str), 
                             int(hour_str), int(minute_str), int(second_str), int(ms_str))


def datetime_to_timestamp(dt):
    return dt.timestamp()


def timestamp_to_datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)
