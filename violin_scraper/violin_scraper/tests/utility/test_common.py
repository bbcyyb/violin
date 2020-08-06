from violin_scraper.utility import common
import datetime
import unittest
import ddt

test_str_datetime_data = [
    ('2020-06-27 22:03:20.642914', datetime.datetime(2020, 6, 27, 22, 3, 20, 642914)),
    ('2020-06-27 22:03:20', datetime.datetime(2020, 6, 27, 22, 3, 20)),
    ('2020-06-27 22:03:00', datetime.datetime(2020, 6, 27, 22, 3)),
    ('2020-06-27', datetime.datetime(2020, 6, 27)),
    ]


@ddt.ddt
class TestCommon(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_datetime_to_timestamp(self):
        dt = datetime.datetime(2020, 8, 6, 22, 35, 12)
        timestamp = common.datetime_to_timestamp(dt)
        self.assertEqual(timestamp, 1596724512)

    def test_timestamp_to_datetime(self):
        timestamp = 1596724512
        result = common.timestamp_to_datetime(timestamp)
        dt = datetime.datetime(2020, 8, 6, 22, 35, 12)
        self.assertEqual(result, dt)

    @ddt.data(*test_str_datetime_data)
    @ddt.unpack
    def test_str_to_datetime(self, str_datetime, dt):
        result = common.str_to_datetime(str_datetime)
        self.assertEqual(result, dt)
