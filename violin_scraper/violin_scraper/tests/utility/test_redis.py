from violin_scraper.utility.redis import Redis
import unittest

HOST = '127.0.0.1'
PORT = 6379
PASS = 'mypass'


class TestRedis(unittest.TestCase):

    # TODO: Use DDT. refer: https://blog.csdn.net/xm_csdn/article/details/107705674

    def test_upper(self):
        self.str_entities = {
            'str_1': 'abcdefg',
            'str_2': '123',
            'str_3':
            '{"title": "str3", "num_list": [ 1,2,3,4,5,6 ], "str_list": [ "aaa", "bbb", "ccc" ]'
        }

    def setUp(self):
        self.r = Redis(None)
        self.assertEqual(self.r.is_connected(), False)
        self.r.connect(host=HOST, port=PORT, password=PASS)
        self.assertEqual(self.r.is_connected(), True)

    def tearDown(self):
        pass

    def test_getstr(self):
        for k, v in self.str_entities:
            self.r.set_str(k, v)

        value1 = self.r.get_str(self.str_entities.keys[0])
        self.assertEqual(value1, self.str_entities.str_1)