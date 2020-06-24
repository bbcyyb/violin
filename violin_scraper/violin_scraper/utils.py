from scrapy import shell
from enum import Enum

import os

def inspect(response, spider):
    spider.logger.info('========> Start inspecting')
    shell.inspect_response(response, spider)
    spider.logger.info('<======== Finish inspecting')

def running_path():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class File:
    def __init__(self, logger = None):
        self._file = None
        self._logger = logger
        pass

    def open_file(self, file, mode='a', buffering=-1, encoding = 'utf-8', errors = None, newline = None, closefd = True, opener = None):
        self._file = open(file, mode, buffering, encoding, errors, newline, closefd, opener)

    def close_file(self):
        if not self.get_status() == FileStatus.Opened:
            self._file_.close()

    def get_status(self):
        if self._file is None:
            return FileStatus.Uninitialized
        if not self._file.closed:
            return FileStatus.Opened
        else:
            return FileStatus.Closed

    def write(self, str, auto_flush):
        self._file.write(str)
        self._log(str)
        if auto_flush:
            self.flush()

    def writeline(self, str, auto_flush):
        strline = '{}\n'.format(str)
        self.write(strline, auto_flush)

    def flush(self):
        self._file.flush()
        
    def _log(self, message):
        if self._logger is not None:
            self._logger.debug(message)

class FileStatus(Enum):
    Uninitialized = 0,
    Opened = 1,
    Closed = 2,
    