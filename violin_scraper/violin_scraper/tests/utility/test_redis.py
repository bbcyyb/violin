from violin_scraper.utility.redis import Redis
from violin_scraper.utility import common
import unittest
import ddt
import json
import datetime

HOST = '127.0.0.1'
PORT = 6379
PASS = 'mypass'

test_str_data = [{
    'str_1': 'abcdefg',
    'str_2': '123',
    'str_3':
    '{"title": "str3", "num_list": [ 4,5,2,10,7,6 ], "str_list": [ "aaa", "bbb", "ccc" ]}'
}]

test_hash_data = [[
    {'key': 'name_1', 'value': '{"cookies": "123456789_hash1", "ttl": \{ttl\}}', 'ttl_offset': 6},
    {'key': 'name_2', 'value': '{"cookies": "123456789_hash2", "ttl": \{ttl\}}', 'ttl_offset': 8},
    {'key': 'name_3', 'value': '{"cookies": "123456789_hash3", "ttl": \{ttl\}}', 'ttl_offset': 9},
    {'key': 'name_1', 'value': '{"cookies": "123456789_hash4", "ttl": \{ttl\}}', 'ttl_offset': 4},
]]


@ddt.ddt
class TestRedis(unittest.TestCase):

    def setUp(self):
        self.r = Redis(None)
        self.assertEqual(self.r.is_connected(), False)
        self.r.connect(host=HOST, port=PORT, password=PASS)
        self.assertEqual(self.r.is_connected(), True)

    def tearDown(self):
        pass

    @ddt.data(*test_str_data)
    def test_str(self, data):
        for k, v in data.items():
            self.r.set_str(k, v)

        for k, v in data.items():
            value = self.r.get_str(k)
            self.assertEqual(value, v)

    @ddt.data(*test_str_data)
    def test_content_update(self, data):
        name = 'str_3'
        j = data[name]
        self.r.set_str(name, j)

        j_value_1 = self.r.get_str(name)
        self.assertEqual(j_value_1, j)
        d_value_1 = json.loads(j_value_1)
        self.assertIsInstance(d_value_1, dict)

        num_list = d_value_1['num_list']
        self.assertEqual(len(num_list), 6)
        num_list.sort(key=lambda n: n, reverse=True)
        self.assertEqual(num_list[-1], 2)
        num_list.pop()
        self.assertEqual(len(num_list), 5)
        self.assertNotEqual(num_list[-1], 2)
        num_list.insert(0, 13)
        num_list.insert(0, 14)

        j2 = json.dumps(d_value_1)
        self.r.set_str(name, j2)

        j_value_2 = self.r.get_str(name)
        d_value_2 = json.loads(j_value_2)
        num_list_2 = d_value_2['num_list']
        self.assertEqual(len(num_list_2), 7)

    @ddt.data(*test_hash_data)
    def test_hash(self, data):
        name = 'test_cookies'

        self.r.delete(name)
        self.assertEqual(len(self.r.getall_hashkeys(name)), 0)

        cur_datetime = datetime.datetime.now().replace(microsecond=0)
        for d in data:
            key = d['key']
            j_value = d['value']
            ttl_offset = d['ttl_offset']

            ttl_date = cur_datetime + datetime.timedelta(seconds=ttl_offset)
            ttl_ts = common.datetime_to_timestamp(ttl_date)
            j_value = j_value.replace('\{ttl\}', str(ttl_ts))
            # d_value = json.loads(j_value)
            self.r.set_hash(name, key, j_value)

        # d_value_arrays = self.r.getall_hash(name)
        # self.assertEqual(len(d_value_arrays), 4)
