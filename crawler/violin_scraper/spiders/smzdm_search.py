import scrapy
from violin_scraper.base_spider import BaseSpider


class SmzdmSearchSpider(BaseSpider):
    name = 'smzdm_search'

    custom_settings = {
        'LOG_FILE': None,
        'DOWNLOADER_MIDDLEWARES': {
            'violin_scraper.middlewares.exception_downloader.ExceptionMiddleware': 120,
            'violin_scraper.middlewares.proxy_downloader.ProxyMiddleware': 543,
            'violin_scraper.middlewares.ua_downloader.UAMiddleware': 544,
        },
        'ITEM_PIPELINES': {
        }
    }

    def start_requests(self):
        urls = ['https://search.smzdm.com/?s={{CONTENT}}&v=b']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_root)

    def parse_root(self, response):
        # response.xpath('//*[@id="feed-main-list"]/li[0]/div/div[2]/h5/a[2]').extract()
        for li in response.xpath('//*[@id="feed-main-list"]/li'):
            a2 = li.xpath('div/div[2]/h5/a[2]')
            pushed_data = a2.xpath('@onclick').extract_first()
            href = a2.xpath('@href').extract_first()
            price = a2.xpath('div/text()').extract_first().split(u'元')[0]
        pass
