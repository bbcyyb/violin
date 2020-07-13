import redis as _redis
from utility.di import service

import logging

_log = logging.getLogger('Redis')

@service
class Redis():
    def __init__(self, context):
        self._rs
        self._pool
        self._is_connected = False

    def connect(self, host='127.0.0.1', port=6379, password=''):
        try:
            self.pool = _redis.ConnectionPool(host=host, port=port, password=password)
            self._rs = _redis.Redis(connection_pool=self.pool)
            self._is_connected = True
        except Exception as e:
            _log.error('Redis connect failed, error info: {}'.format(e))
            self.is_connected = False

    def is_connected(self):
        return self._is_connected

    def disconnect(self):
        if self.is_connected():
            self.pool.disconnect(False)
            self.is_connected = False

    def str_get(self, k):
        res = self._rs.get(k)  # poor performance 
        if res:
            return str(res)

    def str_set(self, k, v, time):
        self._rs.set(k, v, time)
        