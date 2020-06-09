import scrapy

class QxmhwSpider(scrapy.Spider):
    name = 'Qxmhw'
    start_urls = ['https://www.qxmhw.com/search-0-324.html'];

    def parse(self, response):
        pass