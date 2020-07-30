import redis as _redis
from violin_scraper.utility.di import service
from violin_scraper.utility.redlock import Redlock

import logging

_log = logging.getLogger('Redis')


@service
class Redis():
    def __init__(self, context):
        self._rs = None
        self._pool = None
        self._is_connected = False
        self._redlock = None

    def connect(self, host='127.0.0.1', port=6379, password=''):
        try:
            self._pool = _redis.ConnectionPool(host=host,
                                              port=port,
                                              password=password)
            self._rs = _redis.StrictRedis(connection_pool=self._pool)
            self._is_connected = True
            self._redlock = Redlock([self._rs])
            # self._redlock = Redlock([{"host": host, "port": port, "password": password}])
        except Exception as e:
            _log.error('Redis connect failed, error info: {}'.format(e))
            self._is_connected = False

    def is_connected(self):
        return self._is_connected

    def disconnect(self):
        if self.is_connected():
            self._pool.disconnect(False)
            self._is_connected = False

    def get_str(self, name):
        # poor performance
        res = self._rs.get(name)
        if res:
            return str(res)

    def set_str(self, name, value, time=None):
        # TODO: Function Decorators is required here
        mylock = self._redlock.lock(name, 1000)
        if mylock:
            try:
                self._rs.set(name, value, time)
            finally:
                self._redlock.unlock(mylock)

    def get_hash(self, name, key):
        res = self._rs.hget(name, key)
        if res:
            return str(res)

    def set_hash(self, name, key, value):
        self._rs.hset(name, key, value)

    def getall_hash(self, name):
        """
        This function is not the best solution to get all hashs
        If you want to get all hash, please consider below code:
        result = conn.hscan_iter('k4', count=100)
        for item in result:
            print(item)
        """
        res = self._rs.hgetall(name)
        data = {}
        if res:
            data = {str(k): str(v) for k, v in res.items()}
        return data

    def getall_hashkeys(self, name):
        keys = []
        if self._rs.exists(name) and self._rs.type(name) == 'hash':
            keys = self._rs.hkeys(name)
        return keys

    def delete(self, key):
        if self._rs.exists(key):
            self._rs.delete(key)
            return 1
        return 0

    def delete_hashkey(self, name, key):
        if self._rs.hexists(name, key):
            self._rs.hdel(name, key)
            return 1
        return 0

    def clean_alldb(self):
        self._rs.flushall()

    def clean_db(self):
        self._rs.flushdb()

    def clean_hash(self, name):
        keys = self._rs.hkeys(name)
        self._rs.hdel(name, keys)
        return len(keys)
