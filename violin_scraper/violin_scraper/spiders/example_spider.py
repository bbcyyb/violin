import scrapy

class ExampleSpider(scrapy.Spider):
    name = 'example'
    start_urls = [
         'http://lab.scrapyd.cn/'
         ]

    def start_requests(self):
        url = 'http://lab.scrapyd.cn/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = "%stag/%s" % (url, tag)

        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'Conent': quote.css('span.text::text').extract_first(),
                'Author': quote.xpath('span/small/text()').extract_first(),
            }

        next_page = response.css('li.next a::attr("href")').extract_first()

        # for debug
        from scrapy.shell import inspect_response
            inspect_response(response, self)

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
        next_page = response.xpath("//ol/li[@class='next']/a/@href").extract_first()

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
