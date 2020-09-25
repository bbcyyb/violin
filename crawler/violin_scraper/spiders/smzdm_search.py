import scrapy
from violin_scraper.base_spider import BaseSpider


class SmzdmSearchSpider(BaseSpider):
    name = 'smzdm_search'

    custom_settings = {
        'LOG_FILE': None,
        'DOWNLOADER_MIDDLEWARES': {
            'violin_scraper.middlewares.exception_downloader.ExceptionMiddleware': 120,
        },
        'ITEM_PIPELINES': {
        }
    }
