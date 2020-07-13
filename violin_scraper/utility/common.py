from scrapy import shell
from enum import Enum

import os
import datetime


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
    date_str, time_str = str.split(' ')
    year_str, month_str, day_str = date_str.split('-')
    hour_str, minute_str, second_str = time_str.split('.')[0].split(':')
    ms_str = time_str.split('.')[1]

    return datetime.datetime(int(year_str), int(month_str), int(day_str), 
                             int(hour_str), int(minute_str), int(second_str), int(ms_str))
