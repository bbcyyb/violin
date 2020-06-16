import scrapy
from violin_scraper.items import SlctItem

class SlctSpider(scrapy.Spider):
    name = 'slct'
    # start_urls = ['https://www.qxmhw.com/search-0-324.html'];

    # Test
    start_urls = ['https://zhuaicun.com/guonei/senluocaituan.html']
    allowed_domains = ['zhuaicun.com']

    # parse list -> detail -> image
    def parse(self, response):
        # next page
        next_url = response.css('div.update_area div.update_area_content nav.navigation div.nav-links a.next::attr(href)').extract()
        if next_url is not None:
            yield scrapy.follow(next_url, callback = self.parse)

        # detail page
        detail_list = response.css('div.update_area div.update_area_content ul.update_area_lists li a::attr(href)').extract()
        for detail_url in detail_list:
            yield scrapy.Request(detail_url, callback = self.parse_detail)

    def parse_detail(self, response):
        title = response.css('div.item_title h1::text').extract_first()
        name = title.split(' – ')[1]

        # next page

        # image page
        img_selector_list = response.css('div.content_left p img')
        for img_selector in img_selector_list:
            item = SlctItem()
            item['name'] = img_selector.css('img::attr(alt)').extract_first().split(' - ')[1].split(' ')[1]
            item['img_url'] = img_selector.css('img::attr(src)').extract_first()
            yield item
