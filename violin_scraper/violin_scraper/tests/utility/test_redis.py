from violin_scraper.utility.redis import Redis
import unittest
import time

HOST = '127.0.0.1'
PORT = 6379
PASS = 'mypass'


class TestRedis(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_connect(self):
        r = Redis(None)
        self.assertEqual(r.is_connected(), False)
        r.connect(host=HOST, port=PORT, password=PASS)
        self.assertEqual(r.is_connected(), True)
        r.disconnect()
        self.assertEqual(r.is_connected(), False)
        time.sleep(2) 
        r.get_str('zzz')
