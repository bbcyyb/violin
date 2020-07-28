import scrapy
from violin_scraper.base_spider import BaseSpider


class ExampleSpider(BaseSpider):
    name = 'example'
    """
    start_urls = ['http://exercise.kingname.info/exercise_xpath_1.html',
                  'http://exercise.kingname.info/exercise_xpath_2.html']
    """

    def start_requests(self):
        urls = ['http://exercise.kingname.info/exercise_xpath_1.html',
                'http://exercise.kingname.info/exercise_xpath_2.html']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_xpath)

    custom_settings = {
        'LOG_FILE': None,
        'DOWNLOADER_MIDDLEWARES': {
            'violin_scraper.middlewares.exception_downloader.ExceptionMiddleware': 120,
        },
        'ITEM_PIPELINES': {
            'violin_scraper.retinues.example.pipelines.Pipeline': 543,
        },
    }

    def parse_xpath(self, response):
        for ul in response.xpath('/html/body/ul'):
            yield {
                'key': ul.xpath('li[@class="name"]/text()').extract_first(),
                'value': ul.xpath('li[@class="price"]/text()').extract_first(),
            }

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'Conent': quote.css('span.text::text').extract_first(),
                'Author': quote.xpath('span/small/text()').extract_first(),
            }

        next_page = response.css('li.next a::attr("href")').extract_first()

        if next_page is not None:
            yield scrapy.Request(next_page, self.parse)

    def parse_(self, response):
        mingyan = response.css('div.quote')

        for v in mingyan:
            text = v.css('.text::text').extract_first()
            autor = v.css('.author::text').extract_first()
            tags = v.css('.tags .tag::text').extract()
            tags = ','.join(tags)

            fileName = '%s-ana.txt' % autor

            with open(fileName, "a+", encoding="utf-8") as f:
                self.logger.info('[======>] %s' % text)
                f.write(text)
                f.write('\n')
                f.write('Tags: ' + tags)
                f.write('\n------\n')
                f.close()

        # next_page = response.css('li.next a::attr(href)').extract_first()
        next_page = response.xpath(
            "//ol/li[@class='next']/a/@href").extract_first()

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
