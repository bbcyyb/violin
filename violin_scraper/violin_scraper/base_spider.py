import scrapy


class BaseSpider(scrapy.Spider):
    def __init__(self, debug='0', *args, **kwargs):
        debug_int = 0
        try:
            debug_int = int(debug, 0)
        except (ValueError, TypeError):
            self.logger.warning(
                "Incorrect type conversion, debug={}".format(debug))
        debug = debug_int if debug_int > 0 else 0
        self.debug_mode = bool(debug)
        self.logger.info('Debug Mode is {}'.format(
            'Opened' if self.debug_mode else 'Closed'))
        super().__init__(*args, **kwargs)