from violin_scraper.utility.redis import Redis
import unittest
import ddt
import json
import time

HOST = '127.0.0.1'
PORT = 6379
PASS = 'mypass'

test_data = [{
    'str_1': 'abcdefg',
    'str_2': '123',
    'str_3':
    '{"title": "str3", "num_list": [ 4,5,2,10,7,6 ], "str_list": [ "aaa", "bbb", "ccc" ]}'
}]


@ddt.ddt
class TestRedis(unittest.TestCase):

    def test_upper(self):
        self.str_entities = {
        }

    def setUp(self):
        self.r = Redis(None)
        self.assertEqual(self.r.is_connected(), False)
        self.r.connect(host=HOST, port=PORT, password=PASS)
        self.assertEqual(self.r.is_connected(), True)

    def tearDown(self):
        pass

    @ddt.data(*test_data)
    def test_str(self, data):
        for k, v in data.items():
            self.r.set_str(k, v)

        for k, v in data.items():
            value = self.r.get_str(k)
            self.assertEqual(value, v)

    @ddt.data(*test_data)
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
