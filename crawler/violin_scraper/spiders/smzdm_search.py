import scrapy
import json
from violin_scraper.base_spider import BaseSpider
from violin_scraper.retinues.smzdm_search.items import SmzdmSearchItem


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
            href = a2.xpath('@href').extract_first()
            price = a2.xpath('div/text()').extract_first().split(u'元')[0]

            pushed_data_raw = a2.xpath('@onclick').extract_first()
            pushed_data_prefix = 'dataLayer.push('
            pushed_data_suffix = ')'
            pushed_data_str = pushed_data_raw[len(pushed_data_prefix): (-1 * len(pushed_data_suffix))]
            pushed_data_json = json.loads(pushed_data_str)

            item = SmzdmSearchItem()
            item['url'] = href
            item['price'] = price
            item['title'] = pushed_data_json[u'article_title']
            item['keyword'] = pushed_data_json[u'search_keyword']
            item['channel'] = pushed_data_json[u'频道']
            item['platform'] = pushed_data_json[u'商城']
            item['brand'] = pushed_data_json[u'品牌']

        pass
