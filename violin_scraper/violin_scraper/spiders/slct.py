import scrapy
from violin_scraper.base_spider import BaseSpider
from violin_scraper.items import SlctItem
from utility.common import running_path

import os


class SlctSpider(BaseSpider):
    name = 'slct'
    # start_urls = ['https://www.qxmhw.com/search-0-324.html'];

    # Test
    start_urls = ['https://zhuaicun.com/guonei/senluocaituan.html']
    allowed_domains = ['zhuaicun.com']

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'violin_scraper.middlewares.exception_downloader.ExceptionMiddlware': 120,
            'violin_scraper.middlewares.proxy_downloader.ProxyMiddleware': 543,
            'violin_scraper.middlewares.ua_downloader.UAMiddleware': 544,
        },
        'ITEM_PIPELINES': {
            'violin_scraper.pipelines.ImagespiderPipeline': 300,
        },
        'IMAGES_STORE':
        os.path.join(os.path.dirname(os.path.dirname(running_path())),
                     'images'),
    }

    # parse list -> detail -> image
    def parse(self, response):
        # next page
        next_url = response.css(
            'div.update_area div.update_area_content nav.navigation div.nav-links a.next::attr(href)'
        ).extract_first()
        if next_url is not None:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(next_url, callback=self.parse)

        # detail page
        detail_list = response.css(
            'div.update_area div.update_area_content ul.update_area_lists li a::attr(href)'
        ).extract()
        for detail_url in detail_list:
            detail_url = response.urljoin(detail_url)
            yield scrapy.Request(detail_url, callback=self.parse_detail)

    def parse_detail(self, response):
        name = response.css('div.item_title h1::text').extract_first()

        # next page
        next_url = response.css(
            'div.content_left div.nav-links a.prev::attr(href)').extract_first(
            )
        if next_url is not None:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(next_url, callback=self.parse_detail)

        # image page
        img_selector_list = response.css('div.content_left p img')
        title = response.css('div.item_title h1::text').extract_first()
        for img_selector in img_selector_list:
            item = SlctItem()
            item['name'] = title
            img_url = response.urljoin(
                img_selector.css('img::attr(src)').extract_first())
            item['img_url'] = [img_url]
            yield item
