import scrapy
from violin_scraper.base_spider import BaseSpider
from violin_scraper.utils import running_path

import os


class ProxySpider(BaseSpider):
    name = 'proxy'
    _page_threshold = 3

    start_urls = ['http://www.66ip.cn/']
    allowed_domains = ['66ip.cn']

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'violin_scraper.middlewares.ProcessAllExceptionMiddlware': 120,
            'violin_scraper.middlewares.ProxyMiddleware': 543,
            'violin_scraper.middlewares.UAMiddleware': 544,
        },
        'ITEM_PIPELINES': {},
        'IMAGES_STORE': None,
    }

    def parse(self, response):
        # area page
        atags = response.xpath('/html/body/div[3]/table/tr/td/ul/li/a')[1:]
        for atag in atags:
            area_url = atag.xpath('@href').extract_first()
            if area_url is not None:
                area_url = response.urljoin(area_url)
                yield scrapy.Request(area_url, callback=self.parse_ips)

    def parse_ips(self, response):
        # next page, take the first three pages.
        page_name = response.url.split('/')[-1]
        try:
            num = page_name.split('.')[0]
            if num < self._page_threshold:
                next_name = '{}.html'.format(num)
        except Exception:

        # extract IP information