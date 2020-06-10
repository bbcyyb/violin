import scrapy
from violin_scraper.models import ImageItem

class QxmhwSpider(scrapy.Spider):
    name = 'Qxmhw'
    # start_urls = ['https://www.qxmhw.com/search-0-324.html'];

    # Test
    start_urls = ['http://lab.scrapyd.cn/archives/55.html']
    allowed_domains = ['lab.scrapyd.cn']

    def parse(self, response):
        item = ImageItem()
        img_urls = response.css('.post img:attr(src)').extract()
        item['url'] = img_urls
        yield item
