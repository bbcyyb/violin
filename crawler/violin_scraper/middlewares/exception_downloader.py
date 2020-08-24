from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
    ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from twisted.web.client import ResponseFailed
from scrapy.http import HtmlResponse
from scrapy.core.downloader.handlers.http11 import TunnelError
from utility.common import running_path
from utility.file import File
import os
import datetime


class ExceptionMiddleware:
    ALL_EXCEPTIONS = (
                        defer.TimeoutError, TimeoutError, DNSLookupError,
                        ConnectionRefusedError, ConnectionDone, ConnectError,
                        ConnectionLost, TCPTimedOutError, ResponseFailed,
                        IOError, TunnelError)

    def process_response(self, request, response, spider):
        record = '[{}] {}'.format(response.status, response.url)
        if str(response.status).startswith('3') or \
           str(response.status).startswith('4') or \
           str(response.status).startswith('5'):
            f = File(spider.logger)
            to_day = datetime.datetime.now()
            f.open_file(os.path.join(running_path(),
                                     'unhandled_{}_{}_{}_{}.log'
                                     .format(spider.name,
                                             to_day.year,
                                             to_day.month,
                                             to_day.day)))
            f.writeline(record)
            f.close_file()
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.ALL_EXCEPTIONS):
            spider.logger.error('Got exception: {}'.format(exception))
            response = HtmlResponse(url='exception')
            return response

        spider.logger.error('Unhandled exception: {}'.format(exception))