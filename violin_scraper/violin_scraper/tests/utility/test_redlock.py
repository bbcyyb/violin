from violin_scraper.utility.redlock import Redlock, MultipleRedlockException

import unittest

HOST = '127.0.0.1'
PORT = 6379
PASS = 'mypass'


class TestRedlock(unittest.TestCase):

    def setUp(self):
        self.redlock = Redlock([{'host': HOST, 'port': PORT, 'password': PASS}])

    def test_lock(self):
        lock = self.redlock.lock('pants', 100)
        self.assertEqual(lock.resource, 'pants')
        self.redlock.unlock(lock)
        lock = self.redlock.lock('pants', 10)
        self.redlock.unlock(lock)

    def test_blocked(self):
        lock = self.redlock.lock('pants', 1000)
        bad = self.redlock.lock('pants', 10)
        self.assertFalse(bad)
        self.redlock.unlock(lock)

    def test_py3_compatible_encoding(self):
        lock = self.redlock.lock('pants', 1000)
        key = self.redlock.servers[0].get('pants_lock')
        self.assertEqual(lock.key, key)

    def test_ttl_not_int_trigger_exception_value_error(self):
        with self.assertRaises(ValueError):
            self.redlock.lock('pants', 1000.0)

    def test_multiple_redlock_exception(self):
        ex1 = Exception('Redis connection error')
        ex2 = Exception('Redis command timed out')
        exc = MultipleRedlockException([ex1, ex2])
        exc_str = str(exc)
        self.assertIn('connection error', exc_str)
        self.assertIn('command timed out', exc_str)
